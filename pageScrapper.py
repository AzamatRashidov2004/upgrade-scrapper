import requests
import sys
from bs4 import BeautifulSoup
import re
from pageOpener import open_page
import time
import random

# List of user agents to cycle through. Add more if desired.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"
]

def fetch_html(url):
    """# Randomly select a user agent for this request.
    user_agent = random.choice(USER_AGENTS)
    HEADERS = {"User-Agent": user_agent}
    print(f"Using User-Agent: {user_agent}")"""
    # A modern User-Agent to mimic a real browser.
    """(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )"""
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    print(f"Fetching: {url}")
    try:
        response = requests.get(url, headers=HEADERS)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

    if response.status_code != 200:
        print(f"Failed to fetch {url} (status code: {response.status_code})")
        """open_page(url)
        time.sleep(30)
        fetch_html(url)"""
        #fetch_html(url)
        return ""
    return response.text

def parse_product_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('h1', class_='heading-1')
    return title_tag.get_text(strip=True) if title_tag else None

def parse_options(html, header_text, option_key):
    soup = BeautifulSoup(html, 'html.parser')
    options = []
    # Find the header containing the specified text.
    header = soup.find(lambda tag: tag.name == 'h3' and header_text in tag.get_text())
    if header:
        # Get the first <ul> after the header.
        ul = header.find_next('ul')
        if ul:
            for li in ul.find_all('li'):
                button = li.find('button')
                if button:
                    spans = button.find_all('span')
                    if len(spans) >= 2:
                        option_value = spans[0].get_text(strip=True)
                        detail = spans[1].get_text(strip=True)
                        options.append({option_key: option_value, 'detail': detail})
    return options

def parse_options2(html, header_text, option_key):
    soup = BeautifulSoup(html, 'html.parser')
    options = []
    
    # Normalize text by collapsing whitespace.
    def normalize(text):
        return " ".join(text.split())
    
    # Find the header element matching the given text after normalization.
    header = soup.find(lambda tag: tag.name == 'h3' and header_text in normalize(tag.get_text()))
    if header:
        # Locate the next <ul> element with a class containing "grid-cols-2"
        ul = header.find_next('ul', class_=lambda c: c and 'grid-cols-2' in c)
        if ul:
            for li in ul.find_all('li'):
                button = li.find('button')
                if button:
                    # Find spans with classes that contain either "body-1" or "body-2"
                    spans = button.find_all('span', class_=lambda c: c and ('body-1' in c or 'body-2' in c))
                    if len(spans) >= 2:
                        option_value = spans[0].get_text(strip=True)
                        detail = spans[1].get_text(strip=True)
                        options.append({option_key: option_value, 'detail': detail})
        else:
            print(f"Could not find <ul> after header '{header_text}'")
    else:
        print(f"Header with text '{header_text}' not found.")
    return options

def parse_conditions(html):
    res = parse_options2(html, "Select the condition", "condition")
    return res

def parse_processors(html):
    return parse_options(html, "Select the processor", "processor")

def parse_memory(html):
    return parse_options(html, "Select memory", "memory")

def parse_storage(html):
    return parse_options(html, "Select storage", "storage")

def parse_color(html):
    soup = BeautifulSoup(html, 'html.parser')
    colors = []
    header = soup.find(lambda tag: tag.name == 'h3' and "Select the color" in tag.get_text())
    if header:
        ul = header.find_next('ul', class_=lambda c: c and 'grid-cols-2' in c)
        if ul:
            for li in ul.find_all('li'):
                button = li.find('button')
                if button:
                    # Extract color code
                    color_div = button.find("div", attrs={"data-test": "icon"})
                    color_code = None
                    if color_div:
                        inner_div = color_div.find("div", style=True)
                        if inner_div:
                            style_attr = inner_div.get("style")
                            match = re.search(r'background-color\s*:\s*(#[0-9A-Fa-f]{6})', style_attr)
                            if match:
                                color_code = match.group(1)
                    
                    # Extract color name and price
                    text_div = button.find("div", class_="ml-16")
                    if text_div:
                        spans = text_div.find_all('span', recursive=True)
                        if len(spans) >= 2:
                            color_name = spans[0].get_text(strip=True)
                            detail = spans[1].get_text(strip=True)
                            colors.append({
                                'color': color_name,
                                'detail': detail,
                                'color_code': color_code
                            })
    return colors

def scrape(url):
    html = fetch_html(url)
    if not html:
        print(f"Could not retrieve content for {url}")
        return
    
    product_title = parse_product_title(html)
    conditions = parse_conditions(html)
    processors = parse_processors(html)
    memories = parse_memory(html)
    storage_options = parse_storage(html)
    color_options = parse_color(html)
    
    print("Product Title:")
    print(product_title)
    print("\nCondition Options:")
    for item in conditions:
        print(item)
    print("\nProcessor Options:")
    for item in processors:
        print(item)
    print("\nMemory Options:")
    for item in memories:
        print(item)
    print("\nStorage Options:")
    for item in storage_options:
        print(item)
    print("\nColor Options:")
    for item in color_options:
        print(item) 