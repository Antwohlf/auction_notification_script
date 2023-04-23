import json
import requests

from typing import Dict, List, Optional
from requests.models import Response

class Shopgoodwill:
    # using components of https://github.com/scottmconway/shopgoodwill-scripts
    API_ROOT = "https://buyerapi.shopgoodwill.com/api"
    
    def shopgoodwill_err_hook(self, res: Response, *args, **kwargs) -> None:
        res.raise_for_status()
    
    def __init__(self, auth_info: Optional[Dict] = None):
        self.shopgoodwill_session = requests.Session()
        self.shopgoodwill_session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0"
        }
        self.shopgoodwill_session.hooks["response"] = self.shopgoodwill_err_hook
        self.logged_in = False

    def get_query_results(self, query_json: Dict, page_size: Optional[int] = 40) -> List[Dict]:
        query_json["page"] = 1
        query_json["pageSize"] = page_size
        total_listings = list()

        while True:
            query_res = self.shopgoodwill_session.post(Shopgoodwill.API_ROOT + "/Search/ItemListing", json=query_json)
            page_listings = query_res.json()["searchResults"]["items"]

            # empty page
            if not page_listings:
                return total_listings
            else:
                query_json["page"] += 1
                total_listings += page_listings

                # break if we've seen all that we expect to see
                if (len(total_listings) == query_res.json()["searchResults"]["itemCount"]):
                    return total_listings
                

def search_shopgoodwill(search_queries):
    script_class = Shopgoodwill()
    id_tracker = set()

    with open("shopgoodwill_query.json") as sgw_query:
        search_query = json.load(sgw_query)

    email_string = ""
    for search in search_queries:
        print('Searching for ' + search)
        # Update JSON value for searching here
        search_query['searchText'] = search
        search_results = script_class.get_query_results(search_query)
        

        for item in search_results:
            important_content = (item['title'], item['currentPrice'], item['remainingTime'])
            if item['itemId'] not in id_tracker:
                # urllib.request.urlretrieve("http://www.digimouth.com/news/media/2011/09/google-logo.jpg", "local-filename.jpg")
                email_string += str(important_content) + "\n" + "https://shopgoodwill.com/item/" + str(item['itemId']) + '\n'
                id_tracker.add(item['itemId'])
    
    return email_string
        

if __name__ == '__main__':
    search_shopgoodwill()