from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import Dict, Optional
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleDocsIntegrationTool(BaseTool):
    """
    Tool for managing Google Docs integration.
    Handles reading, formatting, and updating captions in Google Docs.
    """
    account_name: str = Field(..., description="Name of the account")
    content: Dict = Field(..., description="Content to be added to Google Docs")
    doc_id: Optional[str] = Field(None, description="Google Doc ID (if not provided, will be read from links.txt)")

    def run(self) -> Dict:
        """
        Updates the Google Doc with new content, applying proper formatting.
        Returns status and metadata about the update.
        """
        # Get document ID from links.txt if not provided
        if not self.doc_id:
            accounts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'accounts')
            links_file = os.path.join(accounts_dir, self.account_name, 'links.txt')
            
            if not os.path.exists(links_file):
                raise FileNotFoundError(f"links.txt not found for account: {self.account_name}")
                
            with open(links_file, 'r') as f:
                lines = f.readlines()
                if len(lines) < 2:
                    raise ValueError("links.txt must contain both Sheet and Doc links")
                # Extract doc_id from the second line (Google Doc link)
                doc_link = lines[1].strip()
                self.doc_id = doc_link.split('/')[-1]

        try:
            # Initialize Google Docs API
            SCOPES = ['https://www.googleapis.com/auth/documents']
            creds = None
            
            # In production, use proper credential management
            # This is a placeholder for credential handling
            if os.path.exists('credentials.json'):
                creds = service_account.Credentials.from_service_account_file(
                    'credentials.json', scopes=SCOPES)
            
            if not creds:
                raise ValueError("Google API credentials not found")
            
            service = build('docs', 'v1', credentials=creds)
            
            # Prepare content
            title = self.content["title"]
            caption = self.content["caption"]
            
            # Create requests for formatting
            requests = [
                # Add title with Heading 3 style
                {
                    'insertText': {
                        'location': {'index': 1},
                        'text': f"{title}\n"
                    }
                },
                {
                    'updateParagraphStyle': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': len(title) + 2
                        },
                        'paragraphStyle': {
                            'namedStyleType': 'HEADING_3',
                            'spaceAbove': {'magnitude': 10, 'unit': 'PT'},
                            'spaceBelow': {'magnitude': 5, 'unit': 'PT'}
                        },
                        'fields': 'namedStyleType,spaceAbove,spaceBelow'
                    }
                },
                # Add caption with normal style
                {
                    'insertText': {
                        'location': {'index': len(title) + 2},
                        'text': f"{caption}\n\n"
                    }
                }
            ]
            
            # Execute the updates
            result = service.documents().batchUpdate(
                documentId=self.doc_id,
                body={'requests': requests}
            ).execute()
            
            return {
                "status": "success",
                "doc_id": self.doc_id,
                "updates": {
                    "title_length": len(title),
                    "caption_length": len(caption)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "doc_id": self.doc_id
            }

if __name__ == "__main__":
    tool = GoogleDocsIntegrationTool(
        account_name="test_account",
        content={
            "title": "Test Title",
            "caption": "Test Caption"
        }
    )
    print(tool.run()) 