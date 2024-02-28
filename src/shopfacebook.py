from playwright.sync_api import sync_playwright
import json

def search_marketplace():
    with open('query_templates/query_facebook.json') as file:
        payload = json.load(file)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f'https://facebook.com/marketplace/{payload["location"]}/search?query={payload["query"]}')
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

            parsed_data = []
            for entry, href in zip(entries, hrefs):
                # Split entry based on newline character to separate title, price, and location
                parts = entry.split('\n')
                # Extract title, price, and location
                title = parts[1]
                price = parts[0]
                location = parts[-1]
                # Append parsed data as a dictionary
                parsed_data.append({
                    'title': title,
                    'price': price,
                    'location': location,
                    'link': 'facebook.com' + href
                })

            for item in parsed_data:
                print(item)
            
            browser.close()

if __name__ == "__main__":
    search_marketplace()
