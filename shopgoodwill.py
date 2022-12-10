import re
import json
import time
import requests
import yagmail
from tqdm import tqdm
import datetime

from typing import Dict, List, Optional
from requests.models import Response

class Shopgoodwill:
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

    
    def send_email(self, itemInfo):
        # using yagmail from https://github.com/kootenpv/yagmail#install
        yag = yagmail.SMTP('anthonywohlfeil@gmail.com', oauth2_file='oauth.json')

        YEAR        = datetime.date.today().year     # the current year
        MONTH       = datetime.date.today().month    # the current month
        DATE        = datetime.date.today().day      # the current day
        HOUR        = datetime.datetime.now().hour   # the current hour
        subjectTime = "New ShopGoodWill Listings - " + str(YEAR) + '/' + str(MONTH) + '/' + str(DATE) + '/' + str(HOUR)

        if itemInfo != "":
            yag.send('anthonywohlfeil@gmail.com', subject = subjectTime, contents = itemInfo)

if __name__ == '__main__':
    scriptClass = Shopgoodwill()
    idTracker = set()

    searchItems = ["post malone vinyl", 
                   "frank ocean", 
                   "weeknd vinyl",
                   "dua lipa vinyl",
                   "zayn vinyl", 
                   "brockhampton vinyl", 
                   "calvin harris vinyl", 
                   "mac miller vinyl", 
                   "neighbourhood vinyl"]


    with open('grace.json') as f:
        queryFile = json.load(f)
        searchQuery = queryFile["query"]

    while(True):
        emailString = ""
        for search in queryFile["searchQueries"]:
            print('Searching for ' + search)
            # Update JSON value here
            searchQuery['searchText'] = search
            searchResults = scriptClass.get_query_results(searchQuery)


            for item in searchResults:
                importantContent = (item['title'], item['currentPrice'], item['remainingTime'])
                if item['itemId'] not in idTracker:
                    emailString += str(importantContent)
                    emailString += "\n"
                    emailString += "https://shopgoodwill.com/item/" + str(item['itemId']) + '\n'
                    idTracker.add(item['itemId'])
        
        scriptClass.send_email(emailString)
        time.sleep(3600)


    '''
    with open('query.json') as f:
        searchQuery = json.load(f)

    while(True):
        emailString = ""
        for search in searchItems:
            print('Searching for ' + search)
            # Update JSON value here
            searchQuery['searchText'] = search
            searchResults = scriptClass.get_query_results(searchQuery)


            for item in searchResults:
                importantContent = (item['title'], item['currentPrice'], item['remainingTime'])
                if item['itemId'] not in idTracker:
                    emailString += str(importantContent)
                    emailString += "\n"
                    emailString += "https://shopgoodwill.com/item/" + str(item['itemId']) + '\n'
                    idTracker.add(item['itemId'])
        
        scriptClass.send_email(emailString)
        time.sleep(3600)
    '''