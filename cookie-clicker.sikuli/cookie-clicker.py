cursor = exists(Pattern("1381305994462.png").targetOffset(-8,9))
    
grandma = exists("1381306302461.png")

farm = exists("1381306326337.png")

factory = exists("1381306337401.png")

mine = exists("1381306355577.png")

shipment = exists("1381306380099.png")

lab = exists("1381306389833.png")

portal = exists("1381306398750.png")

cookie = exists("1381306626003.png")


# challenge: there is not enough contrast in the buttons to make it possible to use sikuli straight off
# THIS REALLY DOES NOT WORK
def buysomething():

    bought = False
 

    
    if(portal):
        click(portal)

    if(lab):
        click(lab)

    if(shipment):
        click(shipment)

    if(mine):
        click(mine)

    if(factory):
        click(factory)

    if(farm):
        click(farm)

    if(grandma):
        click(grandma)
      

    if(cursor):
        click(cursor)
    
    return bought



def cookieclick(n):
    for i in range(1,n):
        click(cookie)

#cookieclick(15)

stop=False

while not stop:
    buy=True

    while buy:
        buy=buysomething()

    cookieclick(10)
    

               