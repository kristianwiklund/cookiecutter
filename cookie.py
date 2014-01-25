#Copyright (c) 2013 Kristian Wiklund
#All rights reserved.

#Redistribution and use in source and binary forms are permitted
#provided that the above copyright notice and this paragraph are
#duplicated in all such forms and that any documentation,
#advertising materials, and other materials related to such
#distribution and use acknowledge that the software was developed
#by the <organization>.  The name of the
#<organization> may not be used to endorse or promote products derived
#from this software without specific prior written permission.
#THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
#IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import timedelta
from selenium.common.exceptions import NoSuchElementException
import time
import urllib 
import re


#from sikuli import *

# open page
#driver = webdriver.Firefox() # yup. crashes firefox ;)
driver = webdriver.Chrome()

inventory = [0,0,0,0,0,0,0,0,0,0]
purchases = []
cps = 0
boughtsomething = False # if at least one thing is bought, we have upgrades

driver.get("http://orteil.dashnet.org/cookieclicker/")
sleep(5); # grace period

starttime = time.time()

assert "Cookie Clicker" in driver.title

# function to read how many cookies we have
def available_cookies():
    cookies = driver.find_element_by_css_selector("div#cookies.title")
    return int(cookies.text.replace(",","").partition(" ")[0])

# function to read CpS
def cookies_per_second():
    cookies = driver.find_element_by_css_selector("div#cookies.title")
    te = cookies.text.replace(",","").partition(":")[2].partition(".")[0]
#    print "cps->"+te+"\n"
    return int(te)

# clicks the big cookie
def click_the_cookie():
    kaka = False
    while not kaka:
        kaka = driver.find_element_by_css_selector("div#bigCookie")
    kaka.click()


# function to parse the info about one upgrade
def parse_upgrade(i):
    # find the upgrade, return the cost
    try:
        u = driver.find_element_by_css_selector("#upgrade"+str(i))
    except NoSuchElementException:
        return False

    #onmouseover contains the info we need.
    m = u.get_attribute("onmouseover")

# look for <span class="price">100</span>

    m = urllib.unquote(m)
    #print m
    #sys.exit()

    p = re.compile('.*<span class="price">([0-9][0-9,]*)</span>.*')
    m = p.sub(r'\1',m)
    m = m.replace(",","")
    print m
    return int(m)

# function to read how many cookies are needed to buy the upgrades
def upgrade_price():

    up = []

    i = 0
    x = True
    while  x != False :
        x = parse_upgrade(i)
        if x != False:
            i=i+1
            up.append(x)

    return up;

# function to read how many cookies are needed to buy the products
# products 0-9
def product_price():

    pp = []

    for i in range(10):
        pp.append(int(driver.find_element_by_css_selector("#product"+str(i)+" .content .price").text.replace(",","")));

    return pp;



# do the actual purchasing of the product
def buy_product(i):
    global cps
    global purchases
    global starttime
    global boughtsomething

    x=driver.find_element_by_css_selector("div#product"+str(i))
    x.click()
    boughtsomething = True

    # update cookies per second
    sleep(1)
    cps = cookies_per_second()

    purchases.append(("product", i, cps, time.time()-starttime))
#    print str(purchases)

def buy_upgrade(i):
    global cps
    global purchases
    global starttime
    global boughtsomething

    x=driver.find_element_by_css_selector("#upgrade"+str(i))
    x.click()
    boughtsomething = True

    # update cookies per second
    sleep(1)
    cps = cookies_per_second()

    purchases.append(("upgrade", i, cps, time.time()-starttime))
#    print str(purchases)

# buy an item if the price is right
# the item must be from minitem to 9, or it won't buy...
def buysomething():
    global costs
    global minitem
#    global inventory
    global purchases
    global boughtsomething
    global ucosts
    
    cookies = available_cookies()

    # upgrades over buildings...
    buyupgrade=-1

    for i in range(0,len(ucosts)):
        if (cookies > ucosts[i]):
            buyupgrade = i

    if buyupgrade > -1:
        print "buying upgrade. cost "+str(ucosts[i])
        buy_upgrade(buyupgrade)
        costs = product_price()
        ucosts = upgrade_price()
        return True

    # try to buy the most expensive thing _with a higher number than minitem_-1, this allows
    # purchasing of the newest item and the second newest item

    buyproduct=-1; 
#    for i in range(minitem-1,10): # initially 0-9
    for i in range(0,10): # initially 0-9
        if(cookies>=costs[i]): # buy if we have enough money
            if i==9:
                buyproduct=i
            else:
                if False: # strategy to never buy more items than the above one
                    if (inventory[i] < inventory[i+1]) or (inventory[i+1]<1):
#                        print "buying. less than i+1 rule\n"
                        buyproduct=i
                else:
                    if (costs[i] < costs[i+1]/3): # buy if less than 1/3 of above
                        buyproduct=i
#                        print "buying. cost < 1/3 of above\n"
                    else:
                        if costs[i] < cps*2: # buy if it takes less than 2 sec to refill
                            buyproduct=i
#                            print "buying. cost < 2*cps\n"

    if buyproduct > -1: # we found something to buy. let's buy it.
        buy_product(buyproduct)
        inventory[buyproduct] = inventory[buyproduct]+1
#        print "bought product "+str(buyproduct)+" new cps: "+str(cps)+" inv: "+str(inventory)+"\n"

        if buyproduct > minitem:
            minitem=buyproduct
            # sell of the older items
            
#            for j in range(0,buyproduct-1):
#                while inventory[j]>0:
#                    sellproduct(j)
#                    sleep(0.1)

        costs = product_price()
        ucosts = upgrade_price()
        return True

    return False

##
## sell one item of something

def sellproduct(i):
    x=driver.find_element_by_css_selector("#rowInfoContent"+str(i)+" + div a")
    
    if x:
        x.click()
        inventory[i] = inventory[i] - 1 
        print "sold something, having "+str(inventory)+"\n"

###
### "main" loop

costs = product_price()
ucosts = []
minitem = 1

# start by stepping up until we can get a cursor

for i in range(15):
    click_the_cookie()
    sleep(0.1)

while True:
    bought = True;
    while bought:
        bought=buysomething()
        
    click_the_cookie()
    sleep(0.1)

                
driver.close();



    
    
    

