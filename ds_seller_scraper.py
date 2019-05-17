from bs4 import BeautifulSoup
import requests
import re

# List of item names to search on eBay
#item_list = ["Mountain Bike", "tv stand", "fridge", "chair", "keyboard", "rack",
#             "bluetooth headphones", "coffee machine", "lamp", "fridge", "wardrobe"]
item_list = ["Mountain Bike"]

def soup_creator(url):
	# Downloads the eBay page for processing
    res = requests.get(url)
    # Raises an exception error if there's an error downloading the website
    res.raise_for_status()
    # Creates a BeautifulSoup object for HTML parsing
    return BeautifulSoup(res.text, 'html.parser')

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

def google_search(item):
    page = requests.get("http://www.google.com/search?q="+item)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
    urls = [re.split(":(?=http)",link["href"].replace("/url?q=",""))[0] for link in links]
    urls = [url for url in urls if "ebay.com" not in url] 
    urls = [url for url in urls if 'google.com' not in url] 
    urls = [url for url in urls if 'webcache' not in url] 
    return urls

# Scrapes and returns list of in demand items listed on eBay search result page
def in_demand_item_finder(urls):
    in_demand_items = []
   
    for url in urls:
        soup = soup_creator(url)
        # Find all items in the results page
        items = soup.findAll(attrs = {'class': 's-item'})

        # This loop checks if the item is "hot" i.e. any of the following 
        # texts are displayed along with the item:
        # number of items remaining, number of buyers watching the item, 
        # item is on sale, number of items sold, etc
        # We stop once we find 20 "hot" items
        x = 0
        for item in items:
            if(x == 3):
                break
            if(item.find("span", {"class": "BOLD NEGATIVE"})):
                num_sold = item.find("span", {"class": "BOLD NEGATIVE"}).get_text()
                # We only look for high demand items that display how many sold next to it
                if(num_sold.find('Sold') != -1):
                    print("num sold/watching: " + num_sold)
                    title = item.find("a", {"class": "s-item__link"}).get_text()
                    link = item.find('a', href=True)
                    in_demand_items.append(link['href'])
                    #print(link['href'] + '\n' + title)
                    x += 1

    print("In demand items found.")
    return in_demand_items

def description_searcher(item_link):
    soup = soup_creator(url)
    

def other_retailer_checker(item_link):
    item_title = ((item_link.lstrip("https://www.ebay.com/itm")).split('/'))[0]
    item_title = re.sub('-', ' ', item_title)
    # Parses the item link to determine the item title
   
    print(google_search(item_title))
    #description_searcher(item_link)
    

# Opens a hot item and determines feedback score of seller
def eBay_item_checker(hot_items):
    x = 0
    for item_link in hot_items:
        if(x == 3):
            break
        soup = soup_creator(item_link)       
        # Finds the feedback score of the seller
        seller_info = soup.find(attrs = {'class': 'mbg-l'})    
        feedback_score = seller_info.find("span", title=True)
        feedback_score = feedback_score['title'].lstrip("feedback score:")


        if((int(feedback_score) > 100) and (int(feedback_score) < 10000)):
            other_retailer_checker(item_link)
            #add_seller(item_link)
        print(feedback_score)
        x += 1

    print("Hot items reviewed.")
    return hot_items
        
links = make_urls(item_list)
hot_items = in_demand_item_finder(links)
eBay_item_checker(hot_items)