from bs4 import BeautifulSoup
import requests

# List of item names to search on eBay
#item_list = ["Mountain Bike", "tv stand", "fridge", "chair", "keyboard", "rack",
#             "bluetooth headphones", "coffee machine", "lamp", "fridge", "wardrobe"]
item_list = ["Mountain Bike"]

# Returns a list of urls that search eBay for an item
def make_urls(names):
    # eBay url that can be modified to search for a specific item on eBay
    url1 = "https://www.ebay.com/sch/i.html?_from=R40&_nkw="
    url2 = "&_sacat=0&_sop=12"
    # List of urls created
    urls = []
    for item in item_list:
        # Adds the name of item being searched to the end of the eBay url and appends it to the urls list
        # In order for it to work the spaces need to be replaced with a +
        urls.append(url1 + item.replace(" ", "+") + url2)

    # Returns the list of completed urls
    print("URL list created.")
    return urls

# Scrapes and returns list of in demand items listed on eBay search result page
def in_demand_item_finder(urls):
    in_demand_items = []
   
    for url in urls:
	    # Downloads the eBay page for processing
	    res = requests.get(url)
	    # Raises an exception error if there's an error downloading the website
	    res.raise_for_status()
	    # Creates a BeautifulSoup object for HTML parsing
	    soup = BeautifulSoup(res.text, 'html.parser')
	    # Find all items in the results page
	    items = soup.findAll(attrs = {'class': 's-item'})

	    # This loop checks if the item is "hot" i.e. any of the following 
	    # texts are displayed along with the item:
	    # number of items remaining, number of buyers watching the item, 
	    # item is on sale, number of items sold, etc
	    # We stop once we find 20 "hot" items
	    x = 0
	    for item in items:
	        if(x == 20):
	            break
	        if(item.find("span", {"class": "BOLD NEGATIVE"})):
	            num_sold = item.find("span", {"class": "BOLD NEGATIVE"}).get_text()
	            # We only look for high demand items that display how many sold next to it
	            if((num_sold.find('Sold') != -1) or (num_sold.find('Watching') != -1)):
	                print("num sold/watching: " + num_sold)
	                title = item.find("a", {"class": "s-item__link"}).get_text()
	                link = item.find('a', href=True)
	                in_demand_items.append(link['href'])
	                x += 1

    print("In demand items found.")
    return in_demand_items
        
links = make_urls(item_list)
in_demand_item_finder(links)