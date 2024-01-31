import json
import requests
import datetime
import re

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
                
    def transform_url(self, url):
        url = url.replace('\\', '/')
        current_month = datetime.datetime.now().strftime('%m')  # Get current month as string
        url = re.sub(r'(t\d)\.jpeg', r'1.jpg', url)
        url = re.sub(r'/items-', f'/Items/{current_month}-', url)  # Insert current month into URL
        return url
    
    def generate_results_object(self, search_queries):
        return True
                

def search_shopgoodwill(search_queries, gw_dupes):
    script_class = Shopgoodwill()

    with open("query_templates/query_goodwill.json") as sgw_query:
        search_query = json.load(sgw_query)

    email_string = ""
    for search in search_queries:
        print('Searching shopgoodwill for ' + search[0])
        # Update JSON value for searching here
        search_query['searchText'] = search[0]
        search_query['highPrice'] = search[1]
        search_results = script_class.get_query_results(search_query)

        # Sort the search results by endTime in ascending order (Ending Soonest)
        sorted_results = sorted(search_results, key=lambda item: item['endTime'])

        if sorted_results:
            email_string += '<strong>' + str(search_query['searchText']) + '</strong>\n'

        item_list = []

        for item in sorted_results:
            # Parse the datetime string and format the datetime object as desired
            datetime_obj = datetime.datetime.fromisoformat(item['endTime'])
            formatted_datetime = datetime_obj.strftime("Ends on %m/%d/%Y at %H:%M:%S UTC")

            # Format the datetime for Google Calendar
            google_calendar_datetime = datetime_obj.strftime("%Y%m%dT%H%M%SZ")

            item_json = {}

            important_content = (item['title'], "$" + str(item['currentPrice']), formatted_datetime)
            if item['itemId'] not in gw_dupes:
                # urllib.request.urlretrieve("http://www.digimouth.com/news/media/2011/09/google-logo.jpg", "local-filename.jpg")
                email_string += "IMGURL:" + script_class.transform_url(item['imageURL']) + "\n" 
                item_json["IMGURL"] = script_class.transform_url(item['imageURL'])
                email_string += "AUCTIONEND:" + google_calendar_datetime + '\n'
                item_json["AUCTIONEND"] = google_calendar_datetime
                email_string += "LINK:" + "https://shopgoodwill.com/item/" + str(item['itemId'])
                item_json["LINK"] = "https://shopgoodwill.com/item/" + str(item['itemId'])
                email_string += "TITLE:" + item['title']
                item_json["TITLE"] = item['title']

                item_json["PRICE"] = item['currentPrice']

                email_string += str(important_content) + "\n"
                gw_dupes.add(item['itemId'])
                item_list.append(item_json)
            

    #return email_string
    return item_list

        

if __name__ == '__main__':
    search_shopgoodwill()