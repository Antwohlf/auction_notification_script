import json
import datetime
import os
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from dotenv import load_dotenv

def configure():
    load_dotenv()

def create_file():
    pass

class ShopEbay:
    def __init__(self):
        self.json_entries = []
        self.payload = {}
        self.log_file = f"EBAY_{datetime.datetime.now().strftime('[%m:%d:%Y, %H]')}"
        
    def load_payload(self):
        with open('query_templates/query_ebay.json') as file:
            self.payload = json.load(file)
            
    def valid_item(self, item, search, eb_dupes):
        # item already found
        if id in eb_dupes:
            return False
        
        # item not lower than max price
        if not (float(item.sellingStatus.currentPrice.value) < float(search["MAX_PRICE"])):
            return False
        
        #is valid item
        return True
    
    def additional_fields(self, item):
        try:
            condition = f'Condition: {item.condition.conditionDisplayName}'
        except:
            condition = ""
        try:
            watchers = f'Watchers: {item.listingInfo.watchCount}'
        except:
            watchers = ""
        try:
            endtime = f'Ends on {item.listingInfo.endTime.strftime("%m/%d/%Y at %H:%M:%S UTC")}'
        except:
            endtime = "None"
        
        return condition, watchers, endtime
    
    def log_entry(self, title, id):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("[%m:%d:%Y, %H:%M:%S]")
        log = f'{formatted_time} - {title} (ID: {id})'
        
        # Ex: [01:01:2024, 08:30:34] - Title of Listing (ID: )
        
        with open(self.log_file, 'w') as file:
            file.write(log)
        

def search_shopebay(search_queries, eb_dupes):
    configure()
    script_class = ShopEbay()
    # json_entries = []
    
    try:
        api = Connection(domain='svcs.ebay.com',appid=os.getenv('ebayauth'), config_file=None)
        script_class.load_payload()
        
        for search in search_queries:
            script_class.payload['keywords'] = search["SEARCH_TERM"]
            script_class.payload['itemFilter'][1]["value"] = search["MAX_PRICE"]
            print('Searching ebay for ' + search["SEARCH_TERM"])

            try:
                response = api.execute('findItemsAdvanced', script_class.payload)
            except:
                continue

            title = ""
            link = ""
            # buyitnow = ""
            condition = ""
            watchers = ""
            # Sort the items by end time in ascending order (Ending Soonest)

            if int(response.reply.searchResult._count) != 0:
                sorted_items = sorted(response.reply.searchResult.item, key=lambda item: item.listingInfo.endTime)
                #result += '<strong>' + str(search[0]) + '</strong>\n'

            for item in sorted_items:
                id = item.itemId
                if script_class.valid_item(item, search, eb_dupes):
                    eb_dupes.add(id)
                else:
                    continue
                
                link = f'{item.viewItemURL}\n'.rstrip()
                
                condition, watchers, endtime = script_class.additional_fields(item)
                
                # buyitnow = f'Buy it now available: : {item.listingInfo.buyItNowAvailable}\n'

                # If item price in acceptable range
                if not (float(item.sellingStatus.currentPrice.value) > float(search["MAX_PRICE"])):
                    json_entry = {"IMGURL": item.galleryURL, "LINK": link, "TITLE": item.title, "AUCTIONEND": endtime, "PRICE": item.sellingStatus.currentPrice.value}
                    if condition:
                        json_entry['Condition'] = condition
                    if watchers:
                        json_entry['Watchers'] = watchers
                    script_class.json_entries.append(json_entry)
                        
        return script_class.json_entries

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


if __name__ == '__main__':
    search_shopebay()