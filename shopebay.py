import datetime
import json
import os
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from dotenv import load_dotenv

# TODO add duplicate protection based on item id in url

def configure():
    load_dotenv()

def search_shopebay():
    configure()
    try:
        api = Connection(domain='svcs.ebay.com',appid=os.getenv('ebayauth'), config_file=None)
        with open('query.json') as file:
            payload = json.load(file)
        
        response = api.execute('findItemsAdvanced', payload)

        assert(response.reply.ack == 'Success')
        assert(type(response.reply.timestamp) == datetime.datetime)
        assert(type(response.reply.searchResult.item) == list)
        result = ""
        title = ""
        buyitnow = ""
        condition = ""
        watchers = ""
        for item in response.reply.searchResult.item:
            title = f'Title: {item.title}, Price: {item.sellingStatus.currentPrice.value}\n'
            buyitnow = f'Buy it now available: : {item.listingInfo.buyItNowAvailable}\n'
            try:
                condition = f'Condition: {item.condition.conditionDisplayName}\n'
            except:
                condition = ""
                pass
            try:
                watchers = f'Watchers: {item.listingInfo.watchCount}\n\n'
            except:
                watchers = ""
                pass
            # print(f'Title: {item.title}, Price: {item.sellingStatus.currentPrice.value}')
            # print(f'Buy it now available: : {item.listingInfo.buyItNowAvailable}\n')
            # try:
            #     print(f'Condition: {item.condition.conditionDisplayName}')
            # except:
            #     pass
            # try:
            #     print(f'Watchers: {item.listingInfo.watchCount}\n')
            # except:
            #     pass
            result += title + buyitnow + condition + watchers
        
        return result



    except ConnectionError as e:
        print(e)
        print(e.response.dict())
    


if __name__ == '__main__':
    search_shopebay()