from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import List, Dict

class UserInputTool(BaseTool):
    """
    Tool for handling user input for caption generation tasks.
    Validates and processes user input for account selection, caption count, and topics.
    """
    account_name: str = Field(..., description="Selected account name")
    caption_count: int = Field(..., description="Number of captions to generate")
    topics: List[str] = Field(..., description="List of topics for caption generation")

    def run(self) -> Dict:
        """
        Validates user input and returns a structured dictionary with the task parameters.
        """
        # Validate caption count
        if self.caption_count < 1:
            raise ValueError("Caption count must be at least 1")
        
        # Validate topics
        if not self.topics:
            raise ValueError("At least one topic must be provided")
        
        return {
            "account": self.account_name,
            "count": self.caption_count,
            "topics": self.topics
        }

if __name__ == "__main__":
    tool = UserInputTool(
        account_name="test_account",
        caption_count=3,
        topics=["marketing", "social media"]
    )
    print(tool.run()) 