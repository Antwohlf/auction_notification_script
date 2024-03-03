from playwright.sync_api import sync_playwright
import json

# TODO investigate why price changes overwrite the item title

def search_marketplace(search_queries, fb_dupes):
    with open('query_templates/query_facebook.json') as file:
        payload = json.load(file)
        location = "annarbor"

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            parsed_data = []

            for query in search_queries:
                page.goto(f'https://facebook.com/marketplace/{location}/search?query={query[0]}')
                page.wait_for_selector('[aria-label="Collection of Marketplace items"]')

                locators = page.locator('[aria-label="Collection of Marketplace items"] a')
                el_count = locators.count()

                entries = []
                hrefs = []

                for index in range(el_count):
                    element = locators.nth(index)
                    inner_text = element.inner_text()
                    href = element.get_attribute('href')

                    entries.append(inner_text)
                    hrefs.append(href)

                for entry, href in zip(entries, hrefs):
                    # Split entry based on newline character to separate title, price, and location
                    parts = entry.split('\n')
                    # Extract title, price, and location
                    title = parts[1]
                    price = parts[0]
                    location = parts[-1]
                    # Append parsed data as a dictionary
                    parsed_data.append({
                        'TITLE': title,
                        'PRICE': price,
                        'LOCATION': location,
                        'LINK': 'facebook.com' + href,
                        'IMGURL': "None", 
                        'AUCTIONEND': 'None'
                    })

            #for item in parsed_data:
            #    print(item)
            
            browser.close()
            return parsed_data

if __name__ == "__main__":
    fb_dupes = set()
    search_queries = [['macbook']]
    results = search_marketplace(search_queries, fb_dupes)
    for item in results:
        print(item)
        print()
    
