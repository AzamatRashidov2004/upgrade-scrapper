#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import time

# A modern User-Agent to mimic a real browser.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}

def get_product_links(url):
    """
    Fetch a URL and parse out product links using BeautifulSoup.
    Adjust the CSS selector if Backmarket's HTML structure changes.
    """
    print(f"Fetching: {url}")
    try:
        response = requests.get(url, headers=HEADERS)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

    if response.status_code != 200:
        print(f"Failed to fetch {url} (status code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    product_links = []

    # Look for the anchor tags wrapping the product cards.
    for a in soup.select('a[data-testid="ProductCard__Wrapper"]'):
        href = a.get("href")
        if href:
            # If the URL is relative, prepend the domain.
            if not href.startswith("http"):
                href = "https://www.backmarket.com" + href
            product_links.append(href)
    
    return product_links

def scrape_category_pages(category_name, urls):
    """
    Scrape a list of URLs for a given category and return unique product links.
    
    :param category_name: The name of the category (for logging).
    :param urls: List of page URLs to scrape.
    :return: List of unique product links.
    """
    print(f"\nScraping category: {category_name}")
    all_links = []
    
    for url in urls:
        links = get_product_links(url)
        print(f"Found {len(links)} links on page: {url}")
        all_links.extend(links)
        time.sleep(1)  # Be polite and wait 1 second between requests.
    
    # Remove duplicates
    unique_links = list(set(all_links))
    print(f"Total unique product links for {category_name}: {len(unique_links)}")
    return unique_links

def main():
    # Define the URLs for each category.
    # iPhones (only Unlocked) – Only one page is provided.
    iphone_urls = [
        "https://www.backmarket.com/en-us/l/iphone/e8724fea-197e-4815-85ce-21b8068020cc?p=0#compatible_carriers=Unlocked"
    ]

    # MacBooks – Provided pages for p=0, p=1, and p=2.
    macbook_urls = [
        "https://www.backmarket.com/en-us/l/apple-macbook/a059fa0c-b88d-4095-b6a2-dcbeb9dd5b33?p=0",
        "https://www.backmarket.com/en-us/l/apple-macbook/a059fa0c-b88d-4095-b6a2-dcbeb9dd5b33?p=1",
        "https://www.backmarket.com/en-us/l/apple-macbook/a059fa0c-b88d-4095-b6a2-dcbeb9dd5b33?p=2"
    ]

    # iPads – Pages p=0 through p=14 (15 pages total).
    ipad_urls = [
        f"https://www.backmarket.com/en-us/l/apple-ipad/f78ae8f5-4611-4ad0-b2ad-ced07765b847?p={page}"
        for page in range(15)
    ]

    # Scrape each category.
    results = {
        "iPhones": scrape_category_pages("iPhones", iphone_urls),
        "MacBooks": scrape_category_pages("MacBooks", macbook_urls),
        "iPads": scrape_category_pages("iPads", ipad_urls)
    }

    # Output the scraped product links.
    for category, links in results.items():
        print(f"\n=== {category} ===")
        for link in links:
            print(link)

if __name__ == "__main__":
    main()
