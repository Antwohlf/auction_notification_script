import shopgoodwill
import shopebay
import yagmail
import datetime
import time
import json
import os

def send_email(email, item_info):
    # using yagmail from https://github.com/kootenpv/yagmail
    yag = yagmail.SMTP(os.getenv('email'), oauth2_file='oauth.json')

    YEAR        = datetime.date.today().year     # the current year
    MONTH       = datetime.date.today().month    # the current month
    DATE        = datetime.date.today().day      # the current day
    HOUR        = datetime.datetime.now().hour   # the current hour
    subject_time = "New ShopGoodWill Listings - " + str(YEAR) + '/' + str(MONTH) + '/' + str(DATE) + '-' + str(HOUR)

    # contents = [yagmail.inline("/path/to/local/image")] to add images later on

    if item_info != "":
        yag.send(email, subject = subject_time, contents = item_info)

if __name__ == '__main__':
    while(True):
        file_name = input('Select a profile: ')
        with open(file_name) as f:
            query_file = json.load(f)
            search_queries = query_file["searchQueries"]
            destination_email = query_file["email"]

        result_goodwill = shopgoodwill.search_shopgoodwill(search_queries)
        #result_ebay = shopebay.search_shopebay()
        result_ebay = "Placeholder"
        email_string = result_goodwill + "\n" + result_ebay + "\n"
        send_email(destination_email, email_string)
        time.sleep(21600)