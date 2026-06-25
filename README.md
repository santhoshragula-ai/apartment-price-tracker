import os
import requests
from bs4 import BeautifulSoup

# The URL of your exact 2-bedroom floor plan layout
TARGET_URL = "https://www.apartments.com/la-costa-plano-tx/vyd5l5d/#74f16hw-2-unit"

# Change this value to whatever you consider a "deal" (e.g., if it drops below $1600)
PRICE_THRESHOLD = 1600 

def check_price():
    # Fetching your API key securely from GitHub secrets
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("Error: SCRAPER_API_KEY is not set!")
        return

    # Using ScrapingAnt to bypass the Apartments.com bot-blocker
    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}"
    
    print("Checking current pricing on Apartments.com...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Target the specific layout section matching your exact link hash
    unit_row = soup.find('div', {'id': '74f16hw-2-unit'})
    
    if unit_row:
        # Find the text that contains the price (usually has a class like 'rentLabel' or 'pricingInfo')
        price_element = unit_row.find(class_='rentLabel') or unit_row.find(class_='pricingInfo')
        
        if price_element:
            price_text = price_element.get_text(strip=True)
            print(f"Found 2-Bedroom Price Text: {price_text}")
            
            # Extract just the numbers (e.g., "$1,650" becomes 1650)
            clean_price = int(''.join(filter(str.isdigit, price_text)))
            
            if clean_price <= PRICE_THRESHOLD:
                print(f"🚨 ALERT! Price dropped to ${clean_price}! Go book it now!")
                # Next step will plug the Telegram/Discord notifier here
            else:
                print(f"Current price is ${clean_price}. Still above your threshold of ${PRICE_THRESHOLD}.")
        else:
            print("Could not locate the price label inside the unit layout.")
    else:
        print("Could not find the specific 2-bedroom floor plan layout on the page.")

if __name__ == "__main__":
    check_price()
