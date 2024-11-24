from pymed import PubMed
import json
import re
from typing import List, Dict

class Article:
    def __init__(self, title : str, keywords: list[str], abstract: str, doi: str, related_dois : list[str]):
        self.title = title
        self.keywords = keywords
        self.abstract = abstract
        self.doi = doi
        self.related_dois = related_dois
    
    def __repr__(self):
        return f"Article(title={self.title}, doi={self.doi})"

    def to_dict(self):
        return {
            'title' : self.title,
            'keywords' : self.keywords,
            'absract' : self.abstract,
            'doi': self.doi,
            'related dois' : self.related_dois
        }

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

            self.results = []
            for article in raw_results:
                title=self.clean_html_tags(article.title if article.title else 'No title available'),
                keywords=article.keywords if article.keywords else [],
                abstract=article.abstract if article.abstract else 'No abstract available',
                doi= str(article.doi.split()[0]) if article.doi else 'No DOI available',
                related_dois=article.doi.split()[1:] if article.doi else []

            
                self.results.append(Article(title, keywords, abstract, doi, related_dois))

        except Exception as e:
            print(f"Error during PubMed query: {e}")
            self.results = []
    
    def write_to_json(self, filename: str) -> bool:
        """
        Writes the results to a JSON file.
        
        Args:
            filename (str): Output filename.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        result_dicts = [article.to_dict() for article in self.results]
        try:
            with open(filename, "w", encoding='utf-8') as outfile:
                json.dump(result_dicts, outfile, indent=4)
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
