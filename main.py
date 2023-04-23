import shopgoodwill
import shopebay
import yagmail
import datetime
import time


def send_email(email, item_info):
        # using yagmail from https://github.com/kootenpv/yagmail
        yag = yagmail.SMTP(EMAIL_HERE, oauth2_file='oauth.json')

        YEAR        = datetime.date.today().year     # the current year
        MONTH       = datetime.date.today().month    # the current month
        DATE        = datetime.date.today().day      # the current day
        HOUR        = datetime.datetime.now().hour   # the current hour
        subject_time = "New Auction Listings - " + str(YEAR) + '/' + str(MONTH) + '/' + str(DATE) + '-' + str(HOUR)

        if item_info != "":
            yag.send(email, subject = subject_time, contents = item_info)

if __name__ == '__main__':
    while(True):
        result_goodwill = shopgoodwill.search_shopgoodwill()
        result_ebay = shopebay.search_shopebay()
        result = result_goodwill + result_ebay
        send_email(EMAIL_HERE, result)
        time.sleep(21600)