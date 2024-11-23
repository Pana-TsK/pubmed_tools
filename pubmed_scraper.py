from pymed import PubMed
import json
import re
from typing import List, Dict

class PubMedClient:
    """A class for querying PubMed and processing results."""
    
    def __init__(self, tool: str, email: str):
        self.pubmed = PubMed(tool=tool, email=email)
        self.results = []
    
    def clean_html_tags(self, text: str) -> str:
        """Removes HTML tags from a string."""
        return re.sub(r"<.*?>", "", text)
    
    def search(self, term: str, max_results: int) -> None:
        """
        Queries PubMed and stores the processed results.
        
        Args:
            term (str): Search query term.
            max_results (int): Maximum number of results to fetch.
        """
        try:
            raw_results = self.pubmed.query(term, max_results=max_results)
            self.results = [
                {
                    'title': self.clean_html_tags(item.get('title', 'No title available')),
                    'keywords': item.get('keywords', 'No keywords available'),
                    'abstract': item.get('abstract', 'No abstract available'),
                    'doi': item.get('doi', 'No DOI available').split()[0]
                }
                for item in (article.toDict() for article in raw_results)
            ]
        except Exception as e:
            print(f"Error during PubMed query: {e}")
            self.results = []
    
    def write_to_txt(self, filename: str) -> bool:
        """
        Writes the results to a text file.
        
        Args:
            filename (str): Output filename.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for i, pub in enumerate(self.results, start=1):
                    file.write(f"{i}\n")
                    file.write(f"Title: {pub['title']}\n")
                    file.write(f"DOI: {pub['doi']}\n")
                    file.write(f"Abstract: {pub['abstract']}\n")
                    file.write("-" * 30 + "\n")
            return True
        except Exception as e:
            print(f"Error writing to text file: {e}")
            return False
    
    def write_to_json(self, filename: str) -> bool:
        """
        Writes the results to a JSON file.
        
        Args:
            filename (str): Output filename.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(filename, "w", encoding='utf-8') as outfile:
                json.dump(self.results, outfile, indent=4)
            return True
        except Exception as e:
            print(f"Error writing to JSON file: {e}")
            return False

def main():
    client = PubMedClient(tool="HygeiaTool", email="panagiotis.tsampanis@ulb.be")
    term = "(Cancer)[title]"
    client.search(term, 10)
    
    if client.write_to_json("cancer.json"):
        print("Results written to results.json")

if __name__ == "__main__":
    main()
