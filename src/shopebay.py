import json
import os
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from dotenv import load_dotenv

def configure():
    load_dotenv()

def search_shopebay(search_queries, eb_dupes):
    configure()

    try:
        api = Connection(domain='svcs.ebay.com',appid=os.getenv('ebayauth'), config_file=None)
        with open('query_templates/query_ebay.json') as file:
            payload = json.load(file)
        
        result = ""
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
            for item in response.reply.searchResult.item:
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
                
                title_price_condition_watchers = f'"{item.title}", ${item.sellingStatus.currentPrice.value}, {condition}, Watchers: {watchers}\n'
                link = f'{item.viewItemURL}\n'
                # buyitnow = f'Buy it now available: : {item.listingInfo.buyItNowAvailable}\n'

                if not (float(item.sellingStatus.currentPrice.value) > float(search[1])):
                    result += title_price_condition_watchers + link
            
        return result

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


if __name__ == '__main__':
    search_shopebay()