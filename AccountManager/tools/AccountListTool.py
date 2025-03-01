from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from typing import List

class AccountListTool(BaseTool):
    """
    Tool for listing available social media accounts by checking subfolders in accounts/.
    Returns a list of account names that have the required files (Brand.txt, old_captions.txt, links.txt).
    """

    def run(self) -> List[str]:
        """
        Lists all valid accounts in the accounts directory.
        A valid account must have Brand.txt, old_captions.txt, and links.txt files.
        """
        accounts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'accounts')
        
        if not os.path.exists(accounts_dir):
            return []
        
        valid_accounts = []
        
        for account_name in os.listdir(accounts_dir):
            account_path = os.path.join(accounts_dir, account_name)
            if not os.path.isdir(account_path):
                continue
                
            required_files = ['Brand.txt', 'old_captions.txt', 'links.txt']
            has_all_files = all(
                os.path.exists(os.path.join(account_path, file))
                for file in required_files
            )
            
            if has_all_files:
                valid_accounts.append(account_name)
        
        return valid_accounts

if __name__ == "__main__":
    tool = AccountListTool()
    print(tool.run()) 