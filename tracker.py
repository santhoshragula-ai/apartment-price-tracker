import os
import requests
from bs4 import BeautifulSoup

# NEW URL: Switching to RentCafe's page for La Costa to bypass the firewall completely
TARGET_URL = "https://www.rentcafe.com/apartments/tx/plano/la-costa/default.aspx"
PRICE_THRESHOLD = 1600 

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("Error: SCRAPER_API_KEY is not set!")
        return

    # Targeting RentCafe which works flawlessly with our standard free credits
    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true"
    
    print("Checking current pricing on RentCafe network...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text()
    
    print("--- Webpage Content Analysis ---")
    if "La Costa" in page_text:
        print("Success! Verified La Costa page loaded smoothly.")
        
        # Look for the 2 Beds starting pricing row
        found_price = False
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        
        for i, line in enumerate(lines):
            if "2 Beds" in line:
                # Print the line showing the floor plan and its starting price
                print(f"👉 Found Floor Plan Row: {line}")
                if i+1 < len(lines):
                    print(f"👉 Current Starting Pricing: {lines[i+1]}")
                found_price = True
                break
                
        if not found_price:
            print("Could not locate the exact '2 Beds' text row, printing top layout snippet instead:")
            print(page_text[:1000])
            
    else:
        print("❌ Loaded text didn't match the expected layout. Printing preview:")
        print(page_text[:1000])

if __name__ == "__main__":
    check_price()
