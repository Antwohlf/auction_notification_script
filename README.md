# Auction Notification Script

As of early 2023, this script is used for searching for a list of queries on ShopGoodWill and Ebay, notifying the user of new items that match those searches via email.

We are currently testing methods for sites such as StockX and Craigslist and will have updates for them later.

## How to use the script
### Getting started
- Pull the repo onto your local workspace
- Run 'pip3 install -r requirements.txt'
- Set up a name.json file for your desired searches profile

### ShopGoodWill Config
This should require no auth config on the user's side.

### Ebay Config
This will require registering for Ebay API access

### Running the script
- Run 'python3 main.py'
- When prompted to add a profile, give the name component of your name.json file (ex: john.json would be passed in as john)
- Let the script run and check your email for search results!
