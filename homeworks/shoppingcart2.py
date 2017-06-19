#Create a new class, called items. Used to define the UPC,name,and price of items in the store
class item(object):
#Dict to store the item names that currently exist.
        inventory = {}
#Do this when an instance of "item" is created
        def __init__(self,name,price):
        #Set the value of THIS INSTANCE's name attribute to the value that was passed in at creation
        #Example  mysoap = item("Irish Sprint",5.99)
                self.name = name
                self.price = price
        # Increment item number
                self.itemno = len(item.inventory) + 1
        #Add the item to the inventory list
                item.inventory[self.itemno] = self
#Define what happens when I call "print mysoap"
        def __str__(self):
                strName = "Item:\t\t%s\n" % self.name
                strPrice = "Price:\t\t$%.2f\n" % self.price
                strItemNo = "ItemNum:\t%04d" % self.itemno
                return strName + strPrice + strItemNo
#Class to store on hand
#This has issues... probably need to change the way I store available items
class mystore(object):
        localstock = {}
        def restock(self,OHitem,qty):
                mystore.localstock[OHitem] = qty
        def __str__(self):
                results = ""
                for x in mystore.localstock:
                        results += "Item: %s\tQty: %s\n" % (x.name,mystore.localstock[x])
                return results
