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
        
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        
        for i, line in enumerate(lines):
            # Look for the row that specifies 2 Bedrooms
            if "2 Beds" in line or "2bd" in line.lower():
                print("\n🎉 TARGET SECTION LOCATED:")
                # Print a block of lines to capture both layout labels and actual numbers
                start = max(0, i)
                end = min(len(lines), i + 5)
                for index in range(start, end):
                    print(f"👉 Line data: {lines[index]}")
                break
    else:
        print("❌ Property confirmation failed on layout.")

if __name__ == "__main__":
    check_price()
