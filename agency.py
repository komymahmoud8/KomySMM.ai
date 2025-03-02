import gradio as gr
from agency_swarm import Agency
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AccountManager.AccountManager import AccountManager
from ContentStrategist.ContentStrategist import ContentStrategist
from ContentWriter.ContentWriter import ContentWriter
from PublishingAgent.PublishingAgent import PublishingAgent
from dotenv import load_dotenv
import json
import uuid

# Load environment variables
load_dotenv()

# Initialize agents
account_manager = AccountManager()
content_strategist = ContentStrategist()
content_writer = ContentWriter()
publishing_agent = PublishingAgent()

# Create agency
agency = Agency([
    account_manager,
    [account_manager, content_strategist],
    [content_strategist, content_writer],
    [content_writer, publishing_agent],
    [account_manager, publishing_agent],
],
    shared_instructions='agency_manifesto.md',
    temperature=0.7,
    max_prompt_tokens=4000
)

# Store workflow states
workflow_states = {}

def list_accounts():
    """List all available accounts"""
    from AccountManager.tools.AccountListTool import AccountListTool
    tool = AccountListTool()
    accounts = tool.run()
    return accounts if accounts else ["No accounts found"]

def generate_captions(account_name: str, num_captions: int, topics: str):
    """Generate initial titles and briefs using the agency"""
    try:
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Convert topics string to list
        topic_list = [t.strip() for t in topics.split(',')]
        
        # Initial message to agency
        initial_message = f"""Please generate {num_captions} social media caption titles and briefs for account '{account_name}' about the following topics: {topics}.
        
        Follow these steps:
        1. Analyze the brand voice and guidelines
        2. Generate engaging titles and briefs
        3. Wait for user approval before proceeding with full captions
        """
        
        # Get completion from the agency
        response = agency.get_completion(initial_message)
        
        # Store workflow state
        workflow_states[task_id] = {
            "account": account_name,
            "topics": topics,
            "num_captions": num_captions,
            "stage": "titles_and_briefs",
            "content": response
        }
        
        return task_id, response
        
    except Exception as e:
        return None, f"Error: {str(e)}"

def submit_feedback(task_id: str, feedback: str, approval: bool):
    """Submit feedback and get revised content"""
    try:
        if task_id not in workflow_states:
            return "Error: Task not found. Please generate new content."
            
        state = workflow_states[task_id]
        current_stage = state["stage"]
        
        if approval:
            # If approved, move to next stage
            if current_stage == "titles_and_briefs":
                # Generate full captions
                message = f"""The titles and briefs have been approved. Please generate the full captions based on the approved content.
                Account: {state['account']}
                Previous response: {state['content']}
                """
                response = agency.get_completion(message)
                state["stage"] = "captions"
                state["content"] = response
                return response
            elif current_stage == "captions":
                # Format and publish
                message = f"""The captions have been approved. Please format and prepare them for publishing.
                Account: {state['account']}
                Previous response: {state['content']}
                """
                response = agency.get_completion(message)
                state["stage"] = "publishing"
                state["content"] = response
                return response
            else:
                # Final stage
                return "Task completed! Content has been formatted and is ready for publishing."
        else:
            # If not approved, revise current stage
            message = f"""Please revise the current content based on the following feedback:
            Account: {state['account']}
            Current content: {state['content']}
            Feedback: {feedback}
            
            Please maintain brand voice and guidelines while addressing the feedback.
            """
            response = agency.get_completion(message)
            state["content"] = response
            return response
            
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="KomySMM_ai - Social Media Caption Generator") as demo:
    gr.Markdown("# KomySMM_ai - Social Media Caption Generator")
    
    # Store task ID
    task_id = gr.State(None)
    
    with gr.Row():
        with gr.Column():
            # Input components
            account_dropdown = gr.Dropdown(
                choices=list_accounts(),
                label="Select Account",
                info="Choose the account to generate captions for"
            )
            num_captions = gr.Slider(
                minimum=1,
                maximum=10,
                value=3,
                step=1,
                label="Number of Captions"
            )
            topics_input = gr.Textbox(
                label="Topics",
                placeholder="Enter topics separated by commas (e.g., marketing, technology, innovation)",
                info="Enter the topics you want to generate captions about"
            )
            generate_btn = gr.Button("Generate Titles & Briefs")
        
        with gr.Column():
            # Output components
            output_text = gr.Textbox(
                label="Generated Content",
                lines=10,
                info="The generated content will appear here"
            )
            
            # Feedback components
            with gr.Row():
                feedback_text = gr.Textbox(
                    label="Feedback",
                    placeholder="Enter your feedback or revision requests here",
                    lines=3
                )
            with gr.Row():
                approve_btn = gr.Button("✓ Approve & Continue", variant="primary")
                revise_btn = gr.Button("↻ Request Revision", variant="secondary")
    
    # Refresh accounts button
    refresh_btn = gr.Button("Refresh Account List")
    
    # Connect components
    def update_task_id_and_output(task_id, response):
        return task_id, response
        
    generate_btn.click(
        generate_captions,
        inputs=[account_dropdown, num_captions, topics_input],
        outputs=[task_id, output_text]
    )
    
    approve_btn.click(
        lambda id, _: submit_feedback(id, "", True),
        inputs=[task_id, feedback_text],
        outputs=output_text
    )
    
    revise_btn.click(
        lambda id, fb: submit_feedback(id, fb, False),
        inputs=[task_id, feedback_text],
        outputs=output_text
    )
    
    refresh_btn.click(
        lambda: gr.Dropdown(choices=list_accounts()),
        outputs=[account_dropdown]
    )

if __name__ == "__main__":
    # Launch the interface
    demo.launch() 
