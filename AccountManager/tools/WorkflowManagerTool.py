from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import Dict, Any, Literal

class WorkflowManagerTool(BaseTool):
    """
    Tool for managing the workflow between different agents.
    Tracks the state of the content creation process and coordinates approvals.
    """
    task_id: str = Field(..., description="Unique identifier for the task")
    action: Literal["start", "update_status", "get_status", "approve", "request_revision"] = Field(
        ..., 
        description="Action to perform on the workflow"
    )
    status_data: Dict[str, Any] = Field(default={}, description="Status data to update")
    feedback: str = Field(default="", description="Feedback for revision requests")

    def run(self) -> Dict:
        """
        Manages workflow state and coordinates between agents.
        """
        # Access shared state for workflow tracking
        workflow_state = self._shared_state.get(f"workflow_{self.task_id}", {})
        
        if self.action == "start":
            # Initialize new workflow
            workflow_state = {
                "status": "in_progress",
                "current_stage": "titles_and_briefs",
                "stages": {
                    "titles_and_briefs": {"status": "in_progress", "content": None, "feedback": []},
                    "captions": {"status": "pending", "content": None, "feedback": []},
                    "publishing": {"status": "pending", "content": None, "feedback": []}
                },
                "account": self.status_data.get("account"),
                "topics": self.status_data.get("topics"),
                "num_captions": self.status_data.get("num_captions")
            }
        
        elif self.action == "update_status":
            # Update workflow state with new data
            if "content" in self.status_data:
                current_stage = workflow_state["current_stage"]
                workflow_state["stages"][current_stage]["content"] = self.status_data["content"]
            workflow_state.update(self.status_data)
        
        elif self.action == "approve":
            current_stage = workflow_state["current_stage"]
            # Mark current stage as approved
            workflow_state["stages"][current_stage]["status"] = "approved"
            
            # Move to next stage
            if current_stage == "titles_and_briefs":
                workflow_state["current_stage"] = "captions"
                workflow_state["stages"]["captions"]["status"] = "in_progress"
            elif current_stage == "captions":
                workflow_state["current_stage"] = "publishing"
                workflow_state["stages"]["publishing"]["status"] = "in_progress"
            elif current_stage == "publishing":
                workflow_state["status"] = "completed"
        
        elif self.action == "request_revision":
            current_stage = workflow_state["current_stage"]
            # Add feedback to current stage
            workflow_state["stages"][current_stage]["feedback"].append(self.feedback)
            workflow_state["stages"][current_stage]["status"] = "needs_revision"
        
        elif self.action == "get_status":
            # Return current workflow state
            return workflow_state
        
        # Store updated state
        self._shared_state.set(f"workflow_{self.task_id}", workflow_state)
        
        return workflow_state

if __name__ == "__main__":
    # Test workflow
    tool = WorkflowManagerTool(
        task_id="test_task_1",
        action="start",
        status_data={
            "account": "Test Account",
            "topics": "test topic",
            "num_captions": 3
        }
    )
    print("Initial state:", tool.run())
    
    # Test update
    tool = WorkflowManagerTool(
        task_id="test_task_1",
        action="update_status",
        status_data={"content": "Test content"}
    )
    print("\nAfter update:", tool.run())
    
    # Test revision request
    tool = WorkflowManagerTool(
        task_id="test_task_1",
        action="request_revision",
        feedback="Please make it more engaging"
    )
    print("\nAfter revision request:", tool.run())
    
    # Test approval
    tool = WorkflowManagerTool(
        task_id="test_task_1",
        action="approve"
    )
    print("\nAfter approval:", tool.run()) 