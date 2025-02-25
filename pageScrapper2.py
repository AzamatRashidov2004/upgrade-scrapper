import requests
import sys
from bs4 import BeautifulSoup
import re
from pageOpener import open_page
import time
import random
from zenrows import ZenRowsClient

# List of user agents to cycle through. Add more if desired.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"
]


proxies = [
    {
        "http": "http://ycevjuot:ztrsoiumv0ct@198.23.239.134:6540",
        "https": "http://ycevjuot:ztrsoiumv0ct@198.23.239.134:6540",
    },
    {
        "http": "http://ycevjuot:ztrsoiumv0ct@207.244.217.165:6712",
        "https": "http://ycevjuot:ztrsoiumv0ct@207.244.217.165:6712",
    },
    {
        "http": "http://ycevjuot:ztrsoiumv0ct@107.172.163.27:6543",
        "https": "http://ycevjuot:ztrsoiumv0ct@107.172.163.27:6543",
    },
    {
        "http": "http://ycevjuot:ztrsoiumv0ct@64.137.42.112:5157",
        "https": "http://ycevjuot:ztrsoiumv0ct@64.137.42.112:5157",
    },
    {
        "http": "http://ycevjuot:ztrsoiumv0ct@173.211.0.148:6641",
        "https": "http://ycevjuot:ztrsoiumv0ct@173.211.0.148:6641",
    },
    {
        "http": "http://ycevjuot:ztrsoiumv0ct@161.123.152.115:6360",
        "https": "http://ycevjuot:ztrsoiumv0ct@161.123.152.115:6360",
    },
    {
        "http": "http://ycevjuot:ztrsoiumv0ct@23.94.138.75:6349",
        "https": "http://ycevjuot:ztrsoiumv0ct@23.94.138.75:6349",
    },
    {
        "http": "http://ycevjuot:ztrsoiumv0ct@154.36.110.199:6853",
        "https": "http://ycevjuot:ztrsoiumv0ct@154.36.110.199:6853",
    },
    {
        "http": "http://ycevjuot:ztrsoiumv0ct@173.0.9.70:5653",
        "https": "http://ycevjuot:ztrsoiumv0ct@173.0.9.70:5653",
    },
    {
        "http": "http://ycevjuot:ztrsoiumv0ct@173.0.9.209:5792",
        "https": "http://ycevjuot:ztrsoiumv0ct@173.0.9.209:5792",
    },
]

isIpad = False



def fetch_html(url, max_retries=5):
    client = ZenRowsClient("16a07b887601abf6db9b310165bdb109eafef870")
    response = client.get(url)
    return response.text
    """#proxy = random.choice(proxies)
    #response = requests.get("https://httpbin.org/ip", proxies=proxy)

    #print(response.text)
    session = requests.Session()
    attempt = 0
    while attempt < max_retries:
        # Randomly select a user agent for each request.
        user_agent = random.choice(USER_AGENTS)
        HEADERS = {
            "User-Agent": user_agent 
        }
        print(f"Fetching: {url} with User-Agent: {user_agent}")
        try:
            response = session.get(url, headers=HEADERS, timeout=10)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            time.sleep(random.uniform(5, 10))  # wait before retrying
            attempt += 1
            continue

        if response.status_code == 200:
            return response.text
        elif response.status_code in [429, 403]:
            print(f"Received {response.status_code} for {url}. Retrying after delay...")
            time.sleep(random.uniform(20, 40))  # longer delay for these errors
            attempt += 1
        else:
            print(f"Failed to fetch {url} (status code: {response.status_code}).")
            return ""
    print(f"Max retries reached for {url}.")
    return """""

def contains_ipad(text):
    """Check if the string contains 'iPad' (case-insensitive)."""
    return "ipad" in text.lower()

def parse_product_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('h1', class_='heading-1')
    res = title_tag.get_text(strip=True) if title_tag else ""
    if contains_ipad(res):
        global isIpad 
        isIpad = True
    else:
        isIpad = False
    return res

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

from bs4 import BeautifulSoup

def parse_conditions_ipad(html):
    """
    Parses device condition options from HTML and returns a list of dictionaries with:
    - name (str)
    - price (str)
    - is_selected (bool)
    - is_good_deal (bool)
    """
    soup = BeautifulSoup(html, 'html.parser')
    conditions_section = soup.find('div', class_='mb-32')
    if not conditions_section:
        return []
    
    conditions = []
    for li in conditions_section.select('ul.grid-cols-2 > li'):
        button = li.find('button')
        if not button:
            continue
            
        # Determine if selected
        is_selected = 'bg-surface-brand-hi' in button.get('class', [])
        
        # Extract condition name
        name_span = button.find('span', class_=['body-1', 'body-1-bold'])
        name = name_span.get_text(strip=True) if name_span else "" 
        
        # Extract price and check for good deal
        price_span = button.find('span', class_='body-2')
        is_good_deal = False
        price = ''
        
        if price_span:
            # Check for good deal icon
            if price_span.find('svg', {'aria-label': 'Good deal'}):
                is_good_deal = True
                # Get text after SVG
                price = ''.join(price_span.find_all(text=True, recursive=False)).strip()
            else:
                price = price_span.get_text(strip=True)
        
        conditions.append({
            'name': name,
            'price': price,
            'is_selected': is_selected,
            'is_good_deal': is_good_deal
        })
    
    return conditions

def parse_storage_ipad(html):
    """
    Parses storage options from HTML and returns a list of dictionaries with:
    - name (str)
    - additional_info (str)
    - is_selected (bool)
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the storage section by its heading
    storage_section = soup.find('p', string='Storage (GB)').find_parent('div', class_='mb-32')
    if not storage_section:
        return []
    
    storages = []
    for li in storage_section.select('ul.grid-cols-3 > li'):
        button = li.find('button')
        if not button:
            continue
            
        # Determine selection state
        is_selected = 'bg-surface-brand-hi' in button.get('class', [])
        
        # Extract storage size
        name_span = button.find('span', class_=['body-1', 'body-1-bold'])
        name = name_span.get_text(strip=True) if name_span else ""
        
        # Extract additional info (empty in example, but might contain text in other cases)
        additional_span = button.find('span', class_='body-2')
        additional_info = additional_span.get_text(strip=True) if additional_span else ''

        storages.append({
            'name': name,
            'additional_info': additional_info,
            'is_selected': is_selected
        })
    
    return storages


def rgb_to_hex(rgb_str):
    """Helper to convert rgb/rgba string to hex format"""
    try:
        values = [int(n) for n in ''.join(c for c in rgb_str if c.isdigit() or c == ',').split(',')[:3]]
        return '#{:02x}{:02x}{:02x}'.format(*values).upper()
    except (ValueError, IndexError):
        return ''
    
def parse_colors_ipad(html):
    """
    Parses color options from HTML and returns a list of dictionaries with:
    - name (str)
    - hex_color (str)
    - is_selected (bool)
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find color section by heading
    color_section = soup.find('p', string='Color').find_parent('div', class_='mb-32')
    if not color_section:
        return []
    
    colors = []
    for li in color_section.select('ul.grid-cols-2 > li'):
        button = li.find('button')
        if not button:
            continue
            
        # Determine selection state
        is_selected = 'bg-surface-brand-hi' in button.get('class', [])
        
        # Extract color name
        name_span = button.find('span', class_=['body-1', 'body-1-bold'])
        name = name_span.get_text(strip=True) if name_span else "" 
        
        # Extract color value and convert to HEX
        color_div = button.find('div', {'data-test': 'icon'})
        hex_color = ''
        if color_div:
            style = color_div.find('div').get('style', '')
            if 'background-color:' in style:
                rgb_str = style.split('background-color:')[-1].strip().rstrip(';')
                hex_color = rgb_to_hex(rgb_str)  # See helper function below

        colors.append({
            'name': name,
            'hex_color': hex_color,
            'is_selected': is_selected
        })
    
    return colors

def parse_conditions(html):
    global isIpad
    if isIpad:
        res = parse_conditions_ipad(html)
    else:
        res = parse_options2(html, "Select the condition", "condition")
    return res

def parse_processors(html):
    return parse_options(html, "Select the processor", "processor")

def parse_memory(html):
    return parse_options(html, "Select memory", "memory")

def parse_storage(html):
    global isIpad
    if isIpad:
        res = parse_storage_ipad(html)
    else:
        res = parse_options(html, "Select storage", "storage")
    return res

def parse_color(html):
    global isIpad
    if isIpad:
        return parse_colors_ipad(html)
    else:
        soup = BeautifulSoup(html, 'html.parser')
        colors = []
        header = soup.find(lambda tag: tag.name == 'h3' and ("Select the color" or "Color") in tag.get_text())
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
    
    data = {
        "url": url,
        "product_title": parse_product_title(html),
        "conditions": parse_conditions(html),
        "processors": parse_processors(html),
        "memories": parse_memory(html),
        "storage_options": parse_storage(html),
        "color_options": parse_color(html)
    }
    
    return data