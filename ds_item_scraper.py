from bs4 import BeautifulSoup
from datetime import *
import requests
import re
import time
start = time.process_time()

# List of seller names to search on eBay. Enter names of sellers like this:
# sellers_list = ["sellername1", "sellername2"]
sellers_list = [""]

# This will create a soup from the url so the webpage can be parsed
def soup_creator(url):
      headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
      }
      # Downloads the eBay page for processing
      res = requests.get(url, headers=headers)
      # Raises an exception error if there's an error downloading the website
      res.raise_for_status()
      # Creates a BeautifulSoup object for HTML parsing
      return BeautifulSoup(res.text, 'lxml')

# Returns a list containing seller result urls. Each url leads to a 
# results page that shows 200 relevant items currently sold by the seller
def make_urls(names):
      # eBay url that can be modified to search for a specific seller on eBay   
      url1 = "https://www.ebay.com/sch/i.html?_sofindtype=0&_\
      byseller=1&_nkw=&_in_kw=1&_ex_kw=&_sacat=0&_udlo=&_udhi=\
      &_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_\
      sadis=15&_stpos=12110-3252&_sargn=-1%26saslc%3D1&_salic=1&_\
      fss=1&_fsradio=%26LH_SpecificSeller%3D1&_saslop=1&_sasl="
      url2 = "&_sop=12&_dmd=1&_ipg=200&_fosrp=1"
      # List of urls created
      urls = []
      for seller in sellers_list:
            # Adds the name of seller being searched to the end of the eBay url and appends it to the urls list
            urls.append(url1 + seller + url2)
      # Returns the list of completed urls
      print("Seller's item results page URLs created.")
      return urls

# returns links to each item in the results page
def item_link_finder(urls):
      item_links = []   
      for url in urls:
            soup = soup_creator(url)
            # Find all items in the results page
            items = soup.findAll(attrs = {'class': 'lvtitle'})
            #we find the link for each item
            x = 0
            for item in items:            
                  link = item.find('a', href=True)
                  item_links.append(link['href'])
                  #if(x==3):
                    #print(link['href'])
                  x += 1
      print("Found item links.")
      return item_links

# Opens an item and determines if the item has a link that shows its purchase history
# If it does have purchase history link then the item is also in demand
def in_demand_item_finder(items):
  purchase_history_links = []
  x = 0
  #check characteristics of each item for first 20 items
  for item_link in items:
        if(x == 20):
            break  
        soup = soup_creator(item_link)    
        # find the price of item  
        item_price_ebay = ((soup.find(attrs = {'class': 'notranslate'}).get_text()).split("$"))[1]
        item_price_ebay = (item_price_ebay.split(".")[0])
        # we only want to sell items between 15 and 200 dollars
        if(float(item_price_ebay) > 200 or float(item_price_ebay) < 15):
            continue
        # tries to find links to item purchase history
        purchase_history_link = soup.find('div', attrs={'class' : 'nonActPanel'})
        if(purchase_history_link.find(href=True)):             
            purchase_history_link = purchase_history_link.find(href=True)
            purchase_history_links.append(purchase_history_link['href'])
            #print(purchase_history_link['href'])
        x += 1
  print("Found item purchase history links.")
  return purchase_history_links

def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1

# Opens an item and checks if it sold at least 4 times in past month
def recently_sold(purchase_history_links):
    print("Finding Items that sold at least 4 times in past month")
    todaysdate = str(date.today())
    current_year = todaysdate.split('-')[0].split('20')[1]
    current_month = todaysdate.split('-')[1]
    current_day = todaysdate.split('-')[2]
    # check each purchase history of each item that has purchase history 
    for purchase_history_link in purchase_history_links:
        x = 0
        soup = soup_creator(purchase_history_link)
        if(soup.find('th', text=re.compile('Date of Purchase'))):
            table = soup.find('th', text=re.compile('Date of Purchase')).find_parent('table')
            # checks the date of each time this item was purchased
            for row in table.find_all('tr')[1:]:
                # output item link if this item sold at least 4 times
                if(x == 4):
                    item_link = soup.find('div', attrs={'class' : 'itemTitle'})
                    item_link = item_link.find('a', href=True)
                    print(item_link['href'])
                    break
                _,_, price_cell, qty_cell, date_cell, *_ = row.find_all('td')
                purchase_date = date_cell.text.strip().split()[0]
                purchase_month = int(month_converter(purchase_date.split('-')[0]))
                purchase_year = int(purchase_date.split('-')[2])
                purchase_day = int(purchase_date.split('-')[1])
                # check if this item was sold in past month
                if(purchase_year == int(current_year)):
                    if(purchase_month == int(current_month)):
                        x+=1
                    elif(purchase_month == int(current_month)-1):
                        if(purchase_day >= int(current_day)):
                            x+=1

seller_item_for_sale = make_urls(sellers_list)
items = item_link_finder(seller_item_for_sale)
purchase_history_links = in_demand_item_finder(items)
recently_sold(purchase_history_links)
print(time.process_time() - start)
