from src.shopgoodwill import search_shopgoodwill
from src.shopebay import search_shopebay
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

def send_email(email, item_info):

    #print(item_info)
    try:
        # using yagmail from https://github.com/kootenpv/yagmail
        yag = yagmail.SMTP(os.getenv('email'), oauth2_file='oauth.json')
        YEAR        = datetime.date.today().year     # the current year
        MONTH       = datetime.date.today().month    # the current month
        DATE        = datetime.date.today().day      # the current day
        HOUR        = datetime.datetime.now().strftime("%H")   # the current hour
        subject_time = "New Goodwill/Ebay Listings" + " " + str(MONTH) + '/' + str(DATE) + '/' + str(YEAR) + ' - ' + str(HOUR) + ":00 UTC"

        # contents can be a list of elements including strings and yagmail.inline objects
        contents = []
        for line in item_info.split('\n'):
            if line.startswith('IMGURL:'):
                # The line is an image URL, so add it as an HTML img tag with specified width and height
                img_url = line[7:]
                contents.append(f'<img src="{img_url}" alt="Image" width="200" height="200">')
            elif line.startswith('LINK:'):
                link = line[5:]
                print("LINK")
                print(link)
                print('\n')
                title = re.search(r'^TITLE:.*', link, re.MULTILINE)
                print("TITLE")
                print(title)
                print('\n')
                '''
                contents.append(f'<a href="{link}">' + title[6:] + '</a>')  '''
            elif line.startswith('AUCTIONEND:'):
                # The line is an auction end time, so add it as a Google Calendar event link
                auction_end = line[12:]
                event_name = 'Auction+End'
                event_url = f'https://www.google.com/calendar/render?action=TEMPLATE&text={event_name}&dates={auction_end}/{auction_end}'
                contents.append(f'<a href="{event_url}">Add to Google Calendar</a>')                
            else:
                # The line is not an image URL, so add it as a string
                contents.append(line)

        if contents:
            yag.send(email, subject = subject_time, contents = contents)

    except Exception as e:
        print(f"Failed to send email. Error: {e}")

## TODO FIX this naming when the above function is deleted
def send_email_standardized(destination_email, results_shopgoodwill, results_ebay):
    # using yagmail from https://github.com/kootenpv/yagmail
    yag = yagmail.SMTP(os.getenv('email'), oauth2_file='oauth.json')

    YEAR        = datetime.date.today().year               # the current year
    MONTH       = datetime.date.today().month              # the current month
    DATE        = datetime.date.today().day                # the current day
    HOUR        = datetime.datetime.now().strftime("%H")   # the current hour
    time_string = str(MONTH) + '/' + str(DATE) + '/' + str(YEAR) + ' - ' + str(HOUR) + ":00 UTC"
    subject_time = "New Goodwill/Ebay Listings " + time_string

    # contents can be a list of elements including strings and yagmail.inline objects
    contents = []

    # SHOPGOODWILL RUN
    contents.append("<h3 style='text-transform: uppercase;'>ShopGoodWill Results:</h3>\n")
    try:
        for item in results_shopgoodwill:
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
        print(f"Issue encountered with ShopGoodwill script - Error: {e}")

    # EBAY RUN
    #TODO ADD END TIME
    contents.append("<h3 style='text-transform: uppercase;'>Ebay Results:</h3>\n")
    try:
        for item in results_ebay:
            # The line is an image URL, so add it as an HTML img tag with specified width and height
            img_url = item["IMGURL"]
            contents.append(f'<img src="{img_url}" alt="Image" width="200" height="200">')

            title = item["TITLE"]
            link = item["LINK"]
            contents.append(f'<a href="{link}">' + title + '</a>')

            price = item["PRICE"]
            contents.append("Current Price: " + price)

            auction_end = item["AUCTIONEND"]
            event_name = 'Auction+End'
            contents.append("Auction End:" + auction_end)
            event_url = f'https://www.google.com/calendar/render?action=TEMPLATE&text={event_name}&dates={auction_end}/{auction_end}'
            contents.append(f'<a href="{event_url}">Add to Google Calendar</a>') 
    except Exception as e:
        print(f"Issue encountered with Ebay script - Error: {e}")

    if contents:
        yag.send(destination_email, subject = subject_time, contents = contents)

if __name__ == '__main__':
    profile_name = input('Select a profile: ')
    profile_path = "profiles/" + profile_name + ".json"
    gw_dupes, eb_dupes = set(), set()

    while(True):
        with open(profile_path) as f:
            profile = json.load(f)
    
        search_queries = profile["searchQueries"]
        destination_email = profile["email"]



        # NEW RESULTS FORMAT
        results_shopgoodwill = search_shopgoodwill(search_queries, gw_dupes)
        results_ebay = search_shopebay(search_queries, eb_dupes)

        send_email_standardized(destination_email, results_shopgoodwill, results_ebay)

        time.sleep(21600)