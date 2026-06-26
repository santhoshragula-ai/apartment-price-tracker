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
    
    print("Connecting to live data hub...")
    response = requests.get(proxy_url)
    
    if response.status_code != 200:
        print(f"Connection failed: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("====== LIVE LA COSTA PRICING ======\n")
    # RentCafe uses specific data attributes for floor plan tables
    tables = soup.find_all('table') or soup.find_all('div', class_='fp-container')
    
    found = False
    for item in tables:
        text = item.get_text(" | ", strip=True)
        if "2 Beds" in text or "2 Bed" in text:
            print(text)
            found = True
            
    if not found:
        # Fallback: Just print lines containing dollar signs to find the price directly
        lines = [line.strip() for line in soup.get_text().split('\n') if line.strip()]
        for line in lines:
            if "$" in line and ("Bed" in line or "B1" in line or "B2" in line):
                print(f"👉 {line}")

if __name__ == "__main__":
    check_price()
