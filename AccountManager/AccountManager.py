from agency_swarm import Agent

class AccountManager(Agent):
    def __init__(self):
        super().__init__(
            name="AccountManager",
            description="Handles user input, manages workflow and coordinates between agents",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.5,
            max_prompt_tokens=4000
        ) 