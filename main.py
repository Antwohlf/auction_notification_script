from src.shopgoodwill import search_shopgoodwill
from src.shopebay import search_shopebay
from cleantext import clean
import yagmail
import datetime
import time
import json
import os

# Potential TODO paths for expansion
# Facebook - https://github.com/JustSxm/Deals-Scraper
# Craigslist - https://github.com/mislam/craigslist-api

# TODO add section headers for content (xbox controller)
# TODO enable last minute notifications for auctions
# TODO add photos in email

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
    profile_name = input('Select a profile: ')
    profile_path = "profiles/" + profile_name + ".json"
    gw_dupes, eb_dupes = set(), set()

    while(True):
        with open(profile_path) as f:
            profile = json.load(f)
    
        search_queries = profile["searchQueries"]
        destination_email = profile["email"]

        result_goodwill = search_shopgoodwill(search_queries, gw_dupes)
        result_ebay = search_shopebay(search_queries, eb_dupes)

        email_string = ""
        email_string = "SHOPGOODWILL RESULTS:\n" + result_goodwill + "EBAY RESULTS:\n" + result_ebay + "\n"

        send_email(destination_email, clean(email_string, no_emoji=True))
        time.sleep(21600)