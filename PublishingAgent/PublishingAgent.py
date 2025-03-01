from agency_swarm import Agent

class PublishingAgent(Agent):
    def __init__(self):
        super().__init__(
            name="PublishingAgent",
            description="Updates Google Docs and Sheets with approved content",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.5,
            max_prompt_tokens=4000
        ) 