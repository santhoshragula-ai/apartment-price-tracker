import os
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://www.rentcafe.com/apartments/tx/plano/la-costa/default.aspx"
PRICE_THRESHOLD = 1800  # Adjust this to your specific booking budget threshold!

def check_price():
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("Error: SCRAPER_API_KEY is not set!")
        return

    proxy_url = f"https://api.scrapingant.com/v2/general?url={TARGET_URL}&x-api-key={api_key}&browser=true"
    
    print("Checking current pricing on RentCafe network...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # RentCafe groups plans into data tables or specific row blocks
    # Let's target all table rows or blocks containing floor plan text
    found_plans = False
    
    # We find all blocks that mention '2 Bed'
    for row in soup.find_all(['tr', 'div', 'section']):
        row_text = row.get_text(" ", strip=True)
        if "2 Beds" in row_text and "$" in row_text:
            # Clean up duplicates by breaking early once we get the main pricing section
            print("\n🎉 SUCCESS! Found 2-Bedroom Pricing Matrix:")
            print(f"-> {row_text[:150]}")
            found_plans = True
            break

    if not found_plans:
        print("Parsing exact blocks failed. Scanning full webpage summary context:")
        lines = [line.strip() for line in soup.get_text().split('\n') if line.strip()]
        for i, line in enumerate(lines):
            if "2 Beds" in line or "2bd" in line.lower():
                print(f"Line match: {line}")
                if i+1 < len(lines):
                    print(f"Next line: {lines[i+1]}")
                break

if __name__ == "__main__":
    check_price()
