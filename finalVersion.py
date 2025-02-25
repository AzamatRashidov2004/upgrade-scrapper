import pandas as pd
import sys
import json
from pageScrapper2 import scrape

def process_spreadsheet_links(file_path):
    """
    Read product links from a spreadsheet, scrape each page,
    and save the combined results as a JSON file.
    
    Args:
        file_path (str): Path to spreadsheet file (CSV or Excel)
    """
    try:
        # Read spreadsheet
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        # Get unique product links
        links = df['Link'].unique()
        print(f"Found {len(links)} unique product links:\n")
        
        all_results = []
        # Process each link with a randomized delay between requests.
        for idx, link in enumerate(links, 1):
            result = scrape(link)
            if result:
                all_results.append(result)
        
        # Write results to a JSON file
        with open("results.json", "w") as f:
            json.dump(all_results, f, indent=4)
        
        print("Scraping complete. Results saved to results.json")
        return all_results
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Example usage - change this path to your spreadsheet
    spreadsheet_path = "all.xlsx"  
    process_spreadsheet_links(spreadsheet_path)
