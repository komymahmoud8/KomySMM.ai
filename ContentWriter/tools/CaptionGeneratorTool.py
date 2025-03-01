from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import Dict, List
import os

class CaptionGeneratorTool(BaseTool):
    """
    Tool for generating social media captions based on approved titles and briefs.
    Maintains consistency with brand voice and previous successful captions.
    """
    account_name: str = Field(..., description="Name of the account")
    title_data: Dict = Field(..., description="Approved title and brief data")
    max_length: int = Field(default=280, description="Maximum caption length")

    def run(self) -> Dict:
        """
        Generates a caption based on the title, brief, and previous successful captions.
        Returns the generated caption with metadata.
        """
        # Get path to old_captions.txt
        accounts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'accounts')
        captions_file = os.path.join(accounts_dir, self.account_name, 'old_captions.txt')
        
        # Read previous captions for style reference
        previous_captions = []
        if os.path.exists(captions_file):
            with open(captions_file, 'r') as f:
                previous_captions = f.readlines()
        
        # Extract title data
        title = self.title_data["title"]
        brief = self.title_data["brief"]
        guidelines = self.title_data.get("guidelines", [])
        
        # Generate caption using OpenAI
        # Note: In a real implementation, you would use the OpenAI API here
        # This is a placeholder implementation
        caption = f"Generated caption for: {title}\n"
        caption += f"Following brief: {brief}\n"
        if previous_captions:
            caption += f"Maintaining style from {len(previous_captions)} previous captions"
            
        # Ensure caption meets length requirements
        if len(caption) > self.max_length:
            caption = caption[:self.max_length-3] + "..."
            
        return {
            "title": title,
            "caption": caption,
            "metadata": {
                "length": len(caption),
                "guidelines_followed": guidelines,
                "references_used": len(previous_captions)
            }
        }

if __name__ == "__main__":
    tool = CaptionGeneratorTool(
        account_name="test_account",
        title_data={
            "title": "Sample Title",
            "brief": "Sample Brief",
            "guidelines": ["Be concise", "Use emojis"]
        }
    )
    print(tool.run()) 