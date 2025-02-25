import webbrowser
import time
import pyautogui
import sys
import platform

def open_page(url, chrome_path=None):
    """
    Opens a URL in Chrome and reloads the page once.
    
    Args:
        url (str): The URL to open
        chrome_path (str): Optional custom path to Chrome executable
    """
    try:
        # Determine OS and set default Chrome paths
        if platform.system() == 'Windows':
            default_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
        elif platform.system() == 'Darwin':  # macOS
            default_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        else:  # Linux
            default_path = '/usr/bin/google-chrome'

        # Use custom path or default path
        chrome = chrome_path or default_path
        
        # Register Chrome browser
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome))
        
        # Open URL in Chrome
        webbrowser.get('chrome').open(url)
        
        # Wait for page to load
        time.sleep(5)
        
        # Send reload command (Ctrl/Cmd + R)
        if platform.system() == 'Darwin':
            pyautogui.hotkey('command', 'r')
        else:
            pyautogui.hotkey('ctrl', 'r')
            
        print(f"Successfully opened {url} in Chrome and reloaded")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
