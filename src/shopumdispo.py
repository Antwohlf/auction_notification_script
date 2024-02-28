import requests
from bs4 import BeautifulSoup

class ShopUofMDispo:
    def __init__(self):
        self.base_url = "https://dispo.umich.edu/electronics-computers.html"
        self.max_entries_per_page = 36
        self.page_num = 1
        
def search_shopuofmdispo():
    script_class = ShopUofMDispo()
    size = script_class.max_entries_per_page
    while size == script_class.max_entries_per_page:
        # Construct URL for the current page
        url = f"{script_class.base_url}?p={script_class.page_num}&product_list_limit={script_class.max_entries_per_page}"

        # Send a GET request to the URL
        response = requests.get(url)
        # print(response)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all product items
            product_items = soup.find_all('li', class_='item product product-item')
            size = len(product_items)
            # If no products found on the page, break the loop
            if not product_items:
                break

            # Process each product item on the current page
            for product in product_items:
                # Extract product details
                product_name = product.find('strong', class_='product name product-item-name').text.strip()
                try:
                  product_price = product.find('span', class_='price').text.strip()
                except:
                  product_price = 'Auction'
                # Print or store the extracted information as needed
                print("Product:", product_name)
                print("Price:", product_price)
                # print()

            # Increment page counter for the next page
            script_class.page_num += 1
        else:
            print(f"Failed to retrieve page {script_class.page_num}.")
            break


if __name__ == '__main__':
    search_shopuofmdispo()