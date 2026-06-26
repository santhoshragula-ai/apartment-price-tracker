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
    
    print("\n====== ALL DETECTED TABLES ON PAGE ======")
    tables = soup.find_all('table')
    
    if tables:
        for index, table in enumerate(tables):
            table_text = table.get_text(" | ", strip=True)
            # If this table contains floor plan info, dump the entire thing cleanly
            if "Bed" in table_text or "Baths" in table_text:
                print(f"\n[Table #{index + 1} Content]:")
                print(table_text)
    else:
        print("No standard HTML tables found. Scanning fallback layout containers...")
        # Fallback for div-based grids
        for container in soup.find_all('div', class_=lambda c: c and ('fp' in c or 'plan' in c or 'unit' in c)):
            container_text = container.get_text(" | ", strip=True)
            if "2 Bed" in container_text:
                print(f"\n[Grid Block Content]:")
                print(container_text[:500])

if __name__ == "__main__":
    check_price()
