import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define headers to mimic browser behavior
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

# Function to scrape data from a given Backmarket URL
def scrape_backmarket(url):
    print(f"Fetching: {url}")
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch the webpage: {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    # Locate product containers (adjust selectors if needed)
    for item in soup.find_all('div', attrs={'data-spec': 'product-card-content'}):
        try:
            name = item.find('span', class_='body-1-bold line-clamp-2').text.strip()
            print(f"Name: {name}")
            price = item.find('div', attrs={'data-qa': 'productCardPrice'}).text.strip()
            print(f"Price: {price}")
            link = item.find('a', attrs={'rel': 'noreferrer noopener'})['href']
            print(f"Link: {link}")
            
            products.append({
                'Name': name,
                'Price': price,
                'Link': f"https://www.backmarket.com{link}"
            })
        except AttributeError:
            # Skip items with missing data
            continue

    return products

# Main function to handle scraping across multiple categories
def main():
    print("Scraping data from Backmarket...")

    # Define URL lists for each category
    iphone_urls = [
        "https://www.backmarket.com/en-us/l/iphone/e8724fea-197e-4815-85ce-21b8068020cc?p=0#compatible_carriers=Unlocked"
    ]

    macbook_urls = [
        "https://www.backmarket.com/en-us/l/apple-macbook/a059fa0c-b88d-4095-b6a2-dcbeb9dd5b33?p=0",
        "https://www.backmarket.com/en-us/l/apple-macbook/a059fa0c-b88d-4095-b6a2-dcbeb9dd5b33?p=1",
        "https://www.backmarket.com/en-us/l/apple-macbook/a059fa0c-b88d-4095-b6a2-dcbeb9dd5b33?p=2"
    ]

    # iPads pages: from p=0 up to p=14 (15 pages)
    ipad_urls = [f"https://www.backmarket.com/en-us/l/apple-ipad/f78ae8f5-4611-4ad0-b2ad-ced07765b847?p={page}" for page in range(15)]

    # List to collect all products
    all_products = []

    # Scrape iPhones
    for url in iphone_urls:
        print("\nScraping iPhone URL:")
        print(url)
        products = scrape_backmarket(url)
        for product in products:
            product["Category"] = "iPhone"
        all_products.extend(products)
        time.sleep(1)  # Be polite and wait a bit between requests

    # Scrape MacBooks
    for url in macbook_urls:
        print("\nScraping MacBook URL:")
        print(url)
        products = scrape_backmarket(url)
        for product in products:
            product["Category"] = "MacBook"
        all_products.extend(products)
        time.sleep(1)

    # Scrape iPads
    for url in ipad_urls:
        print("\nScraping iPad URL:")
        print(url)
        products = scrape_backmarket(url)
        for product in products:
            product["Category"] = "iPad"
        all_products.extend(products)
        time.sleep(1)

    # Process and save the data if any products were found
    if all_products:
        df = pd.DataFrame(all_products)

        # Clean and process the 'Price' column for sorting
        df['Price'] = (
            df['Price']
            .str.replace('$', '', regex=False)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
            .str.strip()
        )
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

        df = df.sort_values(by='Price', ascending=True)

        # Save the data to an Excel file
        file_name = 'backmarket_products.xlsx'
        df.to_excel(file_name, index=False)
        print(f"\nData has been saved to {file_name}")
    else:
        print("No data found.")

if __name__ == "__main__":
    main()
