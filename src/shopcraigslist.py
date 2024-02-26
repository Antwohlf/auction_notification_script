import requests
import json
from bs4 import BeautifulSoup

def search_shopcraigslist(search_queries, cl_dupes):
    with open('query_templates/query_craigslist.json') as file:
      payload = json.load(file)   
      for search_query in search_queries[0]:
        base_url = f"https://{payload['location']}.craigslist.org/search/"
        params = {'query': search_query, 'excats': 'hhh,housing,jjj,hss,bbb,sss,apa'}
        print('Searching craigslist for ' + search_query)
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            listings = soup.find_all('li', class_='cl-static-search-result')

            results = []
            for listing in listings:
                link = listing.find('a')['href']
                listing_id = link.split("/")[-1]
                if listing_id in cl_dupes:
                  continue
                else:
                  title = listing.find('div', class_='title').text.strip()
                  
                  price_tag = listing.find('div', class_='price')
                  price = price_tag.text.strip() if price_tag else 'None'
                  
                  location_tag = listing.find('div', class_='location')
                  location = location_tag.text.strip() if location_tag else 'None'
                  
                  image_tag = listing.find('img', class_='result-image')
                  image_url = image_tag['src'] if image_tag else 'None'
                  
                  results.append({'TITLE': title, 'PRICE': price, 'LOCATION': location, 'LINK': link, 'IMGURL': image_url, 'AUCTIONEND': 'None'})
            return results
        else:
            print("Failed to retrieve data from Craigslist.")
            return []

# if __name__ == "__main__":
#     search_query = input("Enter your search query: ")
#     results = scrape_craigslist(search_query)
    
#     print(f"Found {len(results)} results for '{search_query}':\n")
#     for i, result in enumerate(results, 1):
#         print(f"{i}. Title: {result['title']}")
#         print(f"   Price: {result['price']}")
#         print(f"   Link: {result['link']}\n")
