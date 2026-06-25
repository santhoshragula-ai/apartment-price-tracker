import requests
from bs4 import BeautifulSoup

# 1. PASTE YOUR APARTMENT URL BETWEEN THE QUOTES BELOW:
URL = "https://www.apartments.com/la-costa-plano-tx/vyd5l5d/#74f16hw-2-unit"

# This hides our script so the website thinks a real Google Chrome browser is visiting
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check_price():
    # Fetch the webpage
    response = requests.get(URL, headers=headers)
    
    # Read the text on the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Print the webpage content to help us find the price text later
    print("--- Webpage Successfully Loaded! ---")
    print(soup.get_text()[:2000]) # Prints the first 2000 characters of text

if __name__ == "__main__":
    check_price()
