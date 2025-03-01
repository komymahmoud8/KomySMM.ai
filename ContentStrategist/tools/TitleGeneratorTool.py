from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import List, Dict

class TitleGeneratorTool(BaseTool):
    """
    Tool for generating post titles and briefs based on brand guidelines and topics.
    Uses brand voice and previous content to maintain consistency.
    """
    brand_info: Dict = Field(..., description="Brand information from BrandAnalyzerTool")
    topics: List[str] = Field(..., description="List of topics to generate titles for")
    count: int = Field(..., description="Number of titles to generate")

    def run(self) -> List[Dict]:
        """
        Generates post titles and briefs based on brand guidelines and topics.
        Returns a list of dictionaries containing titles and briefs.
        """
        # Initialize the result list
        titles_and_briefs = []
        
        # Extract brand elements
        about = self.brand_info.get("about", "")
        core_values = self.brand_info.get("core_values", [])
        tone_guidelines = self.brand_info.get("tone", [])
        dos = self.brand_info.get("dos", [])
        donts = self.brand_info.get("donts", [])
        
        # Generate titles and briefs using brand guidelines
        for i in range(self.count):
            for topic in self.topics:
                title_data = {
                    "title": f"Title {i+1} for {topic}",
                    "brief": f"""Create content about {topic} that:
                    - Aligns with our brand values: {', '.join(core_values[:2])}
                    - Uses our tone guidelines: {', '.join(tone_guidelines[:2])}
                    - DOs: {', '.join(dos[:2])}
                    - DON'Ts: {', '.join(donts[:2])}
                    """,
                    "topic": topic,
                    "guidelines": {
                        "core_values": core_values,
                        "tone": tone_guidelines,
                        "dos": dos,
                        "donts": donts
                    }
                }
                titles_and_briefs.append(title_data)
                
                if len(titles_and_briefs) >= self.count:
                    break
            if len(titles_and_briefs) >= self.count:
                break
        
        return titles_and_briefs[:self.count]

if __name__ == "__main__":
    # Test data
    brand_info = {
        "about": "Test brand description",
        "core_values": ["Value 1", "Value 2"],
        "tone": ["Tone 1", "Tone 2"],
        "dos": ["Do 1", "Do 2"],
        "donts": ["Don't 1", "Don't 2"],
        "checklist": ["Check 1", "Check 2"]
    }
    tool = TitleGeneratorTool(
        brand_info=brand_info,
        topics=["Test Topic"],
        count=1
    )
    print(tool.run()) 