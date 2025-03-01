from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from typing import Dict

class BrandAnalyzerTool(BaseTool):
    """
    Tool for analyzing brand identity from Brand.txt file.
    Extracts and processes brand voice, tone, and guidelines.
    """
    account_name: str = Field(..., description="Name of the account to analyze")

    def run(self) -> Dict:
        """
        Reads and analyzes the Brand.txt file for the specified account.
        Returns structured brand information.
        """
        accounts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'accounts')
        brand_file = os.path.join(accounts_dir, self.account_name, 'Brand.txt')
        
        if not os.path.exists(brand_file):
            raise FileNotFoundError(f"Brand.txt not found for account: {self.account_name}")
        
        with open(brand_file, 'r') as f:
            brand_content = f.read()
        
        # Parse brand content into structured data
        brand_info = {
            "about": "",
            "core_values": [],
            "tone": [],
            "dos": [],
            "donts": [],
            "checklist": []
        }
        
        current_section = None
        for line in brand_content.split('\n'):
            line = line.strip()
            if not line or line == '---':
                continue
            
            # Remove markdown formatting
            line = line.replace('*', '').strip()
            
            # Detect sections
            if line.startswith('### About'):
                current_section = "about"
                continue
            elif line.startswith('### Core Values'):
                current_section = "core_values"
                continue
            elif line.startswith('### Tone of Voice'):
                current_section = "tone"
                continue
            elif line.startswith('### Dos and Don'):
                current_section = "dos_donts"
                continue
            elif line.startswith('### Checklist'):
                current_section = "checklist"
                continue
            elif line.startswith('DO:'):
                current_section = "dos"
                continue
            elif line.startswith('DON\'T:'):
                current_section = "donts"
                continue
            
            # Process content based on section
            if current_section == "about":
                if brand_info["about"]:
                    brand_info["about"] += " " + line
                else:
                    brand_info["about"] = line
            elif current_section == "core_values" and line.startswith(('1.', '2.', '3.', '4.')):
                # Extract value after the colon
                parts = line.split(':', 1)
                if len(parts) > 1:
                    value = parts[1].strip()
                    brand_info["core_values"].append(value)
            elif current_section == "tone" and line.startswith(('Approachable', 'Motivational', 'Simple', 'Exciting', 'Grounded')):
                # Extract description after the colon
                parts = line.split(':', 1)
                if len(parts) > 1:
                    tone = parts[1].strip()
                    brand_info["tone"].append(tone)
            elif current_section == "dos" and line.startswith('-'):
                brand_info["dos"].append(line.strip('- '))
            elif current_section == "donts" and line.startswith('-'):
                brand_info["donts"].append(line.strip('- '))
            elif current_section == "checklist" and line.startswith(('1.', '2.', '3.', '4.', '5.')):
                # Extract the question after the number
                parts = line.split('.', 1)
                if len(parts) > 1:
                    question = parts[1].strip()
                    brand_info["checklist"].append(question)
        
        return brand_info

if __name__ == "__main__":
    tool = BrandAnalyzerTool(account_name="Ytsera Air")
    print(tool.run()) 