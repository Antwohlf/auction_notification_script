# Auction Notification Script

As of mid 2024, this script is used for searching for a list of queries on the following sites
 - ShopGoodWill
 - Ebay
 - Facebook Marketplace
 - Craigslist
notifying the user of new items that match those searches via email at a regular cadence.

We are currently testing methods for other sites such as StockX and AliExpress and will have updates for them later.

## How to use the script
### Getting started
- Pull the repo onto your local workspace
- Run 'pip3 install -r requirements.txt'
- Set up a name.json file for your desired searches profile using the profile.json example from the repo as a reference
  - Include your email in the "email" section so the script knows where to send the notifications

### ShopGoodWill Config
This should require no auth config on the user's side.

### Ebay Config
This will require registering for Ebay API access and keeping your credentials in a LOCAL .env file

### Facebook Marketplace Config
This will require manual selection of a location as the results are localized

### Craigslist Config
This will require manual selection of a location as Craigslist is divided into localized sub domains

### Running the script
- Run 'python3 main.py'
- When prompted to add a profile, give the name component of your name.json file (ex: john.json would be passed in as john)
- Let the script run and check your email for search results!
- [Optional] Run the script using Tmux or Screen to keep it running and updating indefinitely
