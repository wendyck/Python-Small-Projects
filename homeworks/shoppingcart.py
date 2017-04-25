#! /usr/bin/env python

class ShoppingCart(object):

    cart_items = []

    def __init__(self):
        self.name = "whizz bang shopping cart"
        

    def add_item(self, Inventory):
        self.cart_items.append(Inventory);

    def print_cart(self):
        print "cart contents:"
        print "-" * 30
        total = 0.0
        for widget in self.cart_items:
            name = widget.get_name();
            quantity = widget.get_quantity();
            price = widget.get_price();
            num = widget.get_quantity();
            subtotal = price * num;
            total += subtotal;
            print "Item: ", name, ", ", quantity, " at $", price, " each: $", subtotal;
        print "Total Price $", total

class Inventory(object):
    def __init__ (self, item_name, item_price = 0.0, item_quantity=1):
        self.item_name = item_name;
        self.item_price = item_price;
        self.item_quantity = item_quantity;
    
    def get_price(self):
        return self.item_price;
    def get_quantity(self):
        return self.item_quantity;
    def set_quantity(self, increase):
        self.item_quantity += increase;

    def get_name(self):
        return self.item_name;
    def print_purchasable(self):
        print "Item: %s at $%d each" % (self.item_name, self.item_price)
        
        
#inventory object that stores item names, prices, and quantities
        
shoppingcart = ShoppingCart();

iphone = Inventory("iPhone", 2.0, 0)
android = Inventory("Samsung Galaxy", 400.0, 0)

print "Would you like to buy anything?"
print "now available:"
iphone.print_purchasable();
print "Purchase how many?"
i_quantity= raw_input();

iphone.set_quantity(int(i_quantity));

shoppingcart.add_item(iphone);

android.print_purchasable();
print "Purchase how many?"
a_quantity= raw_input();

android.set_quantity(int(a_quantity));

shoppingcart.add_item(android);

shoppingcart.print_cart();
