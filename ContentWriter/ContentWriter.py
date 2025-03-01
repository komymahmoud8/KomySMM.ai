from agency_swarm import Agent

class ContentWriter(Agent):
    def __init__(self):
        super().__init__(
            name="ContentWriter",
            description="Generates captions matching brand tone and style",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.7,
            max_prompt_tokens=4000
        ) 