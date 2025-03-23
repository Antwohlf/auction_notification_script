from src.shopgoodwill import search_shopgoodwill
from src.shopebay import search_shopebay
from src.shopcraigslist import search_shopcraigslist
from src.shopumdispo import search_shopuofmdispo
from src.shopfacebook import search_marketplace
from cleantext import clean
import yagmail
import datetime
import time
import json
import os
import re

# Potential TODO paths for expansion
# Facebook - https://github.com/JustSxm/Deals-Scraper
# Craigslist - https://github.com/mislam/craigslist-api
# AliExpress - https://blog.adnansiddiqi.me/develop-ali-express-scraper-in-python-with-scraper-api/

# TODO link on auction end date to add to google calendar
# TODO enable last minute notifications for auctions

def add_email_content(website_name, contents, results):
    ## TODO update website_name to be constants
    contents.append("<h3 style='text-transform: uppercase;'> " + website_name + " Results:</h3>\n")
    try:
        for item in results:
            # The line is an image URL, so add it as an HTML img tag with specified width and height
            img_url = item["IMGURL"]
            contents.append(f'<img src="{img_url}" alt="Image" width="200" height="200">')

            title = item["TITLE"]
            link = item["LINK"]
            contents.append(f'<a href="{link}">' + title + '</a>')

            price = item["PRICE"]
            contents.append("Price: " + str(price))

            auction_end = item["AUCTIONEND"]
            event_name = 'Auction+End'
            event_url = f'https://www.google.com/calendar/render?action=TEMPLATE&text={event_name}&dates={auction_end}/{auction_end}'
            contents.append(f'<a href="{event_url}">Add to Google Calendar</a>') 
    except Exception as e:
        print(f"Issue encountered with %s script - Error: {e}", website_name)

def send_email_standardized(destination_email, results_shopgoodwill, results_ebay, results_shopcraigslist, results_uofmdispo, results_facebook):
    # using yagmail from https://github.com/kootenpv/yagmail
    yag = yagmail.SMTP(os.getenv('email'), oauth2_file='oauth.json')

    CURRENT_YEAR        = datetime.date.today().year               
    CURRENT_MONTH       = datetime.date.today().month            
    CURRENT_DATE        = datetime.date.today().day               
    CURRENT_HOUR        = datetime.datetime.now().strftime("%H") 
    time_string = str(CURRENT_MONTH) + '/' + str(CURRENT_DATE) + '/' + str(CURRENT_YEAR) + ' - ' + str(CURRENT_HOUR) + ":00 UTC"
    subject_time = "New Item Listings " + time_string # TODO make this a one liner using datetime str formatting

    # Contents can be a list of elements, including strings and yagmail.inline objects
    contents = []

    add_email_content('ShopGoodWill', contents, results_shopgoodwill)
    add_email_content('Ebay', contents, results_ebay)
    add_email_content('Craigslist', contents, results_shopcraigslist)
    add_email_content('Facebook', contents, results_facebook)
    add_email_content('UM Dispo', contents, results_uofmdispo)

    if contents:
        print('CONTENTS --')
        print(contents)
        yag.send(destination_email, subject = subject_time, contents = contents)

if __name__ == '__main__':
    profile_name = input('Select a profile: ')
    profile_path = "profiles/" + profile_name + ".json"
    gw_dupes, eb_dupes, cl_dupes, um_dupes, fb_dupes = set(), set(), set(), set(), set() # TODO make this cleaner

    while(True):
        with open(profile_path) as f:
            profile = json.load(f)
    
        search_queries = profile["searchQueries"]
        destination_email = profile["email"]


        # Initialize results dictionaries
        results_shopgoodwill = {}
        results_ebay = {}
        results_craigslist = {}
        results_uofmdispo = {}
        results_facebook = {}

        # Attempt to fetch results, catching any exceptions and continuing if there's a failure
        try:
            results_shopgoodwill = search_shopgoodwill(search_queries, gw_dupes)
        except Exception as e:
            print(f"Error in search_shopgoodwill: {e}")

        try:
            results_ebay = search_shopebay(search_queries, eb_dupes)
        except Exception as e:
            print(f"Error in search_shopebay: {e}")

        try:
            results_craigslist = search_shopcraigslist(search_queries, cl_dupes)
        except Exception as e:
            print(f"Error in search_shopcraigslist: {e}")

        try:
            results_facebook = search_marketplace(search_queries, fb_dupes)
        except Exception as e:
            print(f"Error in search_marketplace: {e}")

        try:
            results_uofmdispo = search_shopuofmdispo(search_queries, um_dupes)
        except Exception as e:
            print(f"Error in search_ufomdispo: {e}")
        
        send_email_standardized(destination_email, results_shopgoodwill, results_ebay, results_craigslist, results_uofmdispo, results_facebook)

        time.sleep(21600)