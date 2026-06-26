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
        print("Success! Verified La Costa page loaded smoothly.\n")
        
        lines = [line.strip() for line in page_text.split('\n') if line.strip()]
        
        print("====== REAL-TIME 2-BEDROOM PRICE MATRIX ======")
        # Look for the specific floor plan variants B1, B2, B3, B4 on the page
        for i, line in enumerate(lines):
            if line in ["B1", "B2", "B3", "B4"]:
                # Print out the layout model name and the next few rows containing prices
                print(f"🏠 Floor Plan Model: {line}")
                end_index = min(len(lines), i + 6)
                for index in range(i + 1, end_index):
                    # Filter out useless buttons or empty text tags
                    if "$" in lines[index] or "Available" in lines[index]:
                        print(f"   👉 Data: {lines[index]}")
                print("-" * 30)
    else:
        print("❌ Property layout format verification failed.")

if __name__ == "__main__":
    check_price()
