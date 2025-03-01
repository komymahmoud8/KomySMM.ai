from agency_swarm import Agent

class ContentStrategist(Agent):
    def __init__(self):
        super().__init__(
            name="ContentStrategist",
            description="Creates post titles and briefs based on brand guidelines",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.7,
            max_prompt_tokens=4000
        ) 