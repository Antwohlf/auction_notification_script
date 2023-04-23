import datetime
import json
import os
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from dotenv import load_dotenv

# TODO add duplicate protection based on item id in url

def configure():
    load_dotenv()

def search_shopebay(search_queries):
    configure()
    try:
        api = Connection(domain='svcs.ebay.com',appid=os.getenv('ebayauth'), config_file=None)
        with open('examples/example_query_ebay.json') as file:
            payload = json.load(file)
        
        result = ""
        for search in search_queries:
            payload['keywords'] = search
            print(f'Searching ebay for {search}')
            response = api.execute('findItemsAdvanced', payload)

            assert(response.reply.ack == 'Success')
            assert(type(response.reply.timestamp) == datetime.datetime)
            assert(type(response.reply.searchResult.item) == list)
            title = ""
            link = ""
            buyitnow = ""
            condition = ""
            watchers = ""
            for item in response.reply.searchResult.item:
                try:
                    condition = f'Condition: {item.condition.conditionDisplayName}'
                except:
                    condition = ""
                    pass
                try:
                    watchers = f'Watchers: {item.listingInfo.watchCount}\n'
                except:
                    watchers = ""
                    pass
                title = f'"{item.title}", ${item.sellingStatus.currentPrice.value}, {condition}, Watchers: {watchers}\n'
                link = f'{item.viewItemURL}\n'
                # buyitnow = f'Buy it now available: : {item.listingInfo.buyItNowAvailable}\n'

                # result += title + buyitnow + condition + watchers
                result += title + link
            
        return result

    except ConnectionError as e:
        print(e)
        print(e.response.dict())
    


if __name__ == '__main__':
    search_shopebay()