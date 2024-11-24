import os
from pubmed_scraper import Article
import requests
from bs4 import BeautifulSoup

class PDFFetcher:
    def __init__(self, articles: list[Article], download_dir: str = "downloads"):
        """
        Initialize the PDF Fetcher with a list of articles.
        Args:
            articles (List[Article]): List of Article instances.
            download_dir (str): Directory to store downloaded PDFs.
        """
        self.articles = articles
        self.download_dir = download_dir
        
        # Create the download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def fetch_pdfs_from_doi(self) -> None:
        """
        Attempts to download the PDF using the DOI.
        
        Args:
            doi (str): DOI of the article.
        """
        for article in self.articles:
            try:
                doi = article.doi
                page_url = f"https://doi.org/{doi[0]}"

                response = requests.get(page_url, timeout = 10)
                response.raise_for_status()  # Raise an error for bad HTTP status codes

                # Parse the HTML content
                soup = BeautifulSoup(response.content, "html.parser")

                # Find all <a> tags with href attributes
                links = soup.find_all("a", href=True)

                # Look for links ending with .pdf
                for link in links:
                    href = link['href']
                    if href.endswith(".pdf"):
                        # If the link is relative, construct the full URL
                        pdf_url = href if href.startswith("http") else requests.compat.urljoin(url, href)
                        return pdf_url  # Return the first PDF link found

                return None  # No PDF found
            except Exception as e:
                print(f"Error fetching or parsing the URL: {e}")


            



def main():
    title= "test title"
    keywords= "[test keywords, one, two]",
    abstract= "test abstract",
    doi= "10.3322/caac.21772",
    related_dois= "[test related dois, one, two]"

    test_article = [Article(title, keywords, abstract, doi, related_dois)]

    test = PDFFetcher(test_article, "C:/Users/panag/OneDrive/Bureaublad")
    test.fetch_pdfs_from_doi()

if __name__ == "__main__":
    main()