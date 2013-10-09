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

# open page
#driver = webdriver.Firefox() # yup. crashes firefox ;)
driver = webdriver.Chrome()


driver.get("http://orteil.dashnet.org/cookieclicker/");
sleep(5); # grace period

assert "Cookie Clicker" in driver.title

# function to read how many cookies we have
def available_cookies():
    cookies = driver.find_element_by_css_selector("div#cookies.title");
    return int(cookies.text.replace(",","").partition(" ")[0])

# clicks the big cookie
def click_the_cookie():
    driver.find_element_by_css_selector("div#bigCookie").click();

# function to read how many cookies are needed to buy the products
# products 0-9
def product_price():

    pp = []

    for i in range(10):
        pp.append(int(driver.find_element_by_css_selector("#product"+str(i)+" .content .price").text.replace(",","")));

    return pp;

# do the actual purchasing of the product
def buy_product(i):
    x=driver.find_element_by_css_selector("div#product"+str(i))
    x.click()
    sleep(1)

# buy an item if the price is right
# the item must be from minitem to 9, or it won't buy...
def buysomething():
    global costs
    global minitem

    cookies = available_cookies()

    # try to buy the most expensive thing _with a higher number than minitem_!

    buyproduct=-1; # if a product was bought, step the minitem limit if necessary
    for i in range(minitem-1,10): # initially 0-9
        if(cookies>costs[i]): # buy if we have more money
            buyproduct=i;

    if buyproduct>-1:
        buy_product(buyproduct)
        minitem=buyproduct+1
        costs = product_price()
        return True

    return False


###
### "main" loop

costs = product_price()
minitem = 1

while True:
    bought = True;
    while bought:
        bought=buysomething()
        
    click_the_cookie()
#    sleep(0.1)

                
driver.close();



    
    
    

