import os
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://www.rentcafe.com/apartments/tx/plano/la-costa/default.aspx"

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("Error: SCRAPER_API_KEY is not set!")
        return

    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true"
    
    print("Connecting directly to the pricing grid...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text()
    
    print("\n====== SEARCHING ALL RAW TEXT BLOCKS ======")
    lines = [line.strip() for line in page_text.split('\n') if line.strip()]
    
    found = False
    for i, line in enumerate(lines):
        # Look for the exact apartment footprint variants or 2 Bed markers
        if "2 Bed" in line or "2Beds" in line or "B1" in line or "B2" in line:
            print(f"\n📍 Match found on Line {i}: {line}")
            # Print the next 8 lines immediately following the match to expose the dynamic price text
            end_index = min(len(lines), i + 9)
            for index in range(i + 1, end_index):
                print(f"   👉 {lines[index]}")
            found = True
            
    if not found:
        print("No direct floor plan keywords found. Printing top 1000 characters of page content:")
        print(page_text[:1000])

if __name__ == "__main__":
    check_price()
