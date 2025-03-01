from agency_swarm import Agency
from AccountManager.AccountManager import AccountManager
from ContentStrategist.ContentStrategist import ContentStrategist
from ContentWriter.ContentWriter import ContentWriter
from PublishingAgent.PublishingAgent import PublishingAgent

# Initialize agents
account_manager = AccountManager()
content_strategist = ContentStrategist()
content_writer = ContentWriter()
publishing_agent = PublishingAgent()

# Create agency with communication flows
agency = Agency([
    account_manager,  # Account Manager is the entry point
    [account_manager, content_strategist],  # Account Manager can talk to Content Strategist
    [content_strategist, content_writer],  # Content Strategist can talk to Content Writer
    [content_writer, publishing_agent],  # Content Writer can talk to Publishing Agent
    [account_manager, publishing_agent],  # Account Manager can talk to Publishing Agent directly if needed
],
    shared_instructions='agency_manifesto.md',
    temperature=0.7,
    max_prompt_tokens=4000
)

if __name__ == "__main__":
    agency.run_demo()  # Start the agency in terminal 