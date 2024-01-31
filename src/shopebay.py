import json
import os
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from dotenv import load_dotenv

def configure():
    load_dotenv()

def create_file():
    pass

def search_shopebay(search_queries, eb_dupes):
    configure()
    json_entries = []
    try:
        api = Connection(domain='svcs.ebay.com',appid=os.getenv('ebayauth'), config_file=None)
        with open('query_templates/query_ebay.json') as file:
            payload = json.load(file)
        
        for search in search_queries:
            payload['keywords'] = search[0]
            payload['itemFilter'][1]["value"] = search[1]
            print('Searching ebay for ' + search[0])

            try:
                response = api.execute('findItemsAdvanced', payload)
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
                if not (float(item.sellingStatus.currentPrice.value)) < float(search[1]) or (id in eb_dupes):
                    continue
                else:
                    eb_dupes.add(id)
                
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
                
                title_price_condition_watchers = f'"{item.title}", ${item.sellingStatus.currentPrice.value}, {condition}, {watchers}, {endtime}\n'
                link = f'{item.viewItemURL}\n'
                # buyitnow = f'Buy it now available: : {item.listingInfo.buyItNowAvailable}\n'

                # If item price in acceptable range
                if not (float(item.sellingStatus.currentPrice.value) > float(search[1])):
                    json_entry = {"IMGURL": item.galleryURL, "LINK": link, "TITLE": item.title, "AUCTIONEND": endtime, "PRICE": item.sellingStatus.currentPrice.value}
                    if condition:
                        json_entry['Condition'] = condition
                    if watchers:
                        json_entry['Watchers'] = watchers
                    json_entries.append(json_entry)
                        
        return json_entries

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


if __name__ == '__main__':
    search_shopebay()