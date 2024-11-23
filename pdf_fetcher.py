from pubmed_scraper import PubMedClient

class PDFfetcher:
    def __init__(self):
        self.client = PubMedClient(tool = "HygeiaTools", email="panagiotis.tsampanis@ulb.be")

    def PDFfetcher(self, query : str, max_results : int):
        """
        Code uses the pubmed_scraper to return a list of pdf files, 
        by using the dois of the papers to scrape the web for the documents.
        """


def main():
    pass

if __name__ == __main__:
    main()