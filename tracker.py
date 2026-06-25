import os
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://www.apartments.com/la-costa-plano-tx/vyd5l5d/"
PRICE_THRESHOLD = 1600 

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("Error: SCRAPER_API_KEY is not set!")
        return

    # Using free credits but adding browser=true to pretend we are a real Chrome browser
    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true"
    
    print("Checking current pricing on Apartments.com using simulated browser...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text()
    
    print("--- Webpage Content Analysis ---")
    if "La Costa" in page_text:
        print("Success! Successfully loaded the La Costa apartment page.")
        
        # Look for the specific unit code or rent ranges on the page
        unit_section = soup.find(id="74f16hw-2-unit") or soup.find(class_="rentLabel")
        
        if unit_section:
            price_text = unit_section.get_text(strip=True)
            print(f"Found price data: {price_text}")
        else:
            print("Looking for general 2-Bedroom pricing indicators...")
            lines = [line.strip() for line in page_text.split('\n') if line.strip()]
            for i, line in enumerate(lines):
                if "2 Beds" in line or "2bd" in line.lower():
                    start = max(0, i-2)
                    end = min(len(lines), i+5)
                    print("Context found:")
                    print("\n".join(lines[start:end]))
                    break
    elif "Access Denied" in page_text or "Cloudflare" in page_text:
        print("❌ Still blocked by the firewall. We will need to try an alternative approach.")
    else:
        print("Loaded page format unknown.")

if __name__ == "__main__":
    check_price()
