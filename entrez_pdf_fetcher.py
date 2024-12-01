from Bio import Entrez

# Set your email for Entrez (required)
Entrez.email = ""

def get_pmc_pdf(pmid):
    """
Fetch the PMC PDF link using Entrez and a given PubMed ID (PMID).

Args:
    pmid (str): The PubMed ID for which to fetch the PMC PDF link.

Returns:
    str: URL to the PDF if available, otherwise None.
"""
    try:    
        # Step 1: Use elink to find related PMC articles
        handle = Entrez.elink(dbfrom="pubmed", db="pmc", id=pmid, linkname="pubmed_pmc")
        records = Entrez.read(handle)
        handle.close()

        # Step 2: Check for links in the response
        if records and "LinkSetDb" in records[0] and records[0]['LinkSetDb']:
            pmc_links = records[0]['LinkSetDb'][0]['Link']
            if pmc_links:
                pmc_id = pmc_links[0]['Id']
                print(f"Found PMC ID: {pmc_id}")

                # Step 3: Construct the PMC article PDF URL
                pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf/"
                return pdf_url
            else:
                print(f"No PMC links available for PMID: {pmid}")
        else:
            print(f"No PMC links found for PMID: {pmid}")

    except Exception as e:
        print(f"Error retrieving PMC link for PMID {pmid}: {e}")

    # Explicit return for cases with no PDF link
    return None

def main():
    # Example Usage
    pmid = "26409271"  # Replace with your PMID
    pdf_link = get_pmc_pdf(pmid)

    if pdf_link:
        print(f"PDF link: {pdf_link}")
    else:
        print("No PDF link found.")


if __name__ == "__main__":
    main()
