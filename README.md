# eBay Drop Shipping Seller Scraper

## What is Drop Shipping?
Drop shipping or more accurately, retail arbitrage, is a supply chain management method used widely on eBay. It is the practice of buying an item from other retailers such as Amazon, Walmart, Target, etc then selling the item for a higher price on ebay. This practice can be devided into two parts. First the customer orders an item from a seller and gives seller his/her delivery address. Second, the seller orders the item from a retailer at a lower price and sets the delivery address as the original customer's address. Sellers who participate in drop shipping do not need to physically interact with the product they sell. 

## What is the goal of this project?
I created this project for the primary reason of saving time. I recently started drop shipping and faced an obstacle. I had to determine what items to sell on eBay. This means I have to find out what *other* drop shippers are selling. However, finding drop shippers on eBay is a time consuming task, and the following procedure had to be used to determine what to sell as a drop shipper:

1. Search any item from any category then find which item in this category is selling the most. 
2. Check out this item and determine who is selling it. 
3. If the seller of this item has 100 to 10000 feedback score (transactions completed) then he/she is a possible drop shipper. 
4. Copy and search the description or title of this item on other retailer sites.
5. If you find this same item on another retailer for lower price then the seller is definitely a drop shipper. 
6. Now open the seller's eBay profile and find out what other high demand items they are selling.

This process can take few hours by hand just to identify 5-10 drop shippers. I wanted to automate this procedure and create a tool that can give me a list of drop shippers and what they are selling. As of right now, the tool can perform step 4 of the procedure.

## How will this scraper work?
I decided to use beautiful soup 4 html parsing package in this project. My program will search an item then download the results page. The downloaded html page will be turned into a bs4 object so I can analyze the webpage. 


Reference: 
- https://omnianalytics.io/2018/08/28/ebay-web-scrape-tutorial/
- https://hackernoon.com/building-a-web-scraper-from-start-to-finish-bb6b95388184
- https://stackoverflow.com/questions/41527601/python-google-search
