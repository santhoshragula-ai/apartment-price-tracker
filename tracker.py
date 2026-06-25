import os
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://www.apartments.com/la-costa-plano-tx/vyd5l5d/#74f16hw-2-unit"
PRICE_THRESHOLD = 1600 

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("Error: SCRAPER_API_KEY is not set!")
        return

    # UPGRADED SETTINGS: Added proxy_type=residential and browser=true to bypass the Access Denied block
    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&proxy_type=residential&browser=true"
    
    print("Checking current pricing on Apartments.com using advanced residential proxy...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Target the specific layout section matching your exact link hash
    unit_row = soup.find('div', {'id': '74f16hw-2-unit'})
    
    if unit_row:
        price_element = unit_row.find(class_='rentLabel') or unit_row.find(class_='pricingInfo')
        
        if price_element:
            price_text = price_element.get_text(strip=True)
            print(f"Found 2-Bedroom Price Text: {price_text}")
            
            clean_price = int(''.join(filter(str.isdigit, price_text)))
            
            if clean_price <= PRICE_THRESHOLD:
                print(f"🚨 ALERT! Price dropped to ${clean_price}! Go book it now!")
            else:
                print(f"Current price is ${clean_price}. Still above your threshold of ${PRICE_THRESHOLD}.")
        else:
            print("Could not locate the price label inside the unit layout.")
    else:
        # If it still can't find the layout, print a snippet to see what it *did* find
        print("Could not find the specific 2-bedroom floor plan layout section.")
        print("--- Text preview of loaded page ---")
        print(soup.get_text()[:1000])

if __name__ == "__main__":
    check_price()
