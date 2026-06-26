import os
import requests
from bs4 import BeautifulSoup

# Switching to a cleaner endpoint for the same property to bypass the firewall
TARGET_URL = "https://www.forrent.com/tx/plano/la-costa/vyd5l5d"
PRICE_THRESHOLD = 1600 

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("Error: SCRAPER_API_KEY is not set!")
        return

    # ScrapingAnt request targeting ForRent
    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true"
    
    print("Checking current pricing on fallback network...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text()
    
    print("--- Webpage Content Analysis ---")
    if "La Costa" in page_text:
        print("Success! Verified La Costa page loaded smoothly.")
        
        # Look for rent ranges or specific 2-bedroom blocks
        found_price = False
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        for i, line in enumerate(lines):
            if "2 Beds" in line or "2bd" in line.lower() or "2 Bed" in line:
                start = max(0, i-1)
                end = min(len(lines), i+4)
                print("Found matching floor plan data:")
                context = "\n".join(lines[start:end])
                print(context)
                found_price = True
                break
                
        if not found_price:
            print("Could not filter down to the 2-bed block text. Printing snippet:")
            print(page_text[:1000])
            
    else:
        print("Could not verify property name on the loaded page layout.")

if __name__ == "__main__":
    check_price()
