# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 10:59:31 2019

Author: Andrew Jaroncyk
Title: Benny's Burgers
Purpose: A Point of Sale (POS) program that automatically calculates total
value of each individual customer order given options to add to a burger that 
also generates an End of Day Report
"""

# Initialize Price
price = 0.00 

# Initialize Menu Counters
BEEF_COUNT = 0
BEYOND_BEEF_COUNT = 0
DOUBLE_COUNT = 0
TRIPLE_COUNT = 0
CHEESE_COUNT = 0
BACON_COUNT = 0
AVOCADO_COUNT = 0
CHILI_COUNT = 0
FRIES_COUNT = 0
RINGS_COUNT = 0

# Commence Calculations
while True:
    beef_choice = input("Please choose beef(B) or beyond beef(y): ")
    if beef_choice == "B" or beef_choice == "b":
        price += 5.75
        BEEF_COUNT += 1 
    elif beef_choice == "Y" or beef_choice == "y":
        price += 6.25
        BEYOND_BEEF_COUNT += 1
    else:
        beef_choice
        
    extra_patty = input("Would you like to make it a double(D) or a triple(T)? or N: ")
    if extra_patty == "D" or extra_patty == "d":
        price += 2.00
        DOUBLE_COUNT += 1
    elif extra_patty == "T" or extra_patty == "t":
        price += 3.50
        TRIPLE_COUNT += 1
    elif extra_patty == "N" or extra_patty == "n":
        price = price
        
    toppings = input("Would you like to add toppings? Y or N: ")
    if toppings == "Y" or toppings == "y":
        cheese = input("Would you like cheese? (Y or N) ")
        if cheese == "Y" or cheese == "y":
            price += 0.50
            CHEESE_COUNT += 1
        elif cheese == "N" or cheese == "n":
            price = price
        bacon = input("Would you like bacon? (Y or N) ")
        if bacon == "Y" or bacon == "y":
            price += 1.25
            BACON_COUNT += 1
        elif bacon == "N" or bacon == "n":
            price = price
        avocado = input("Would you lke avocado? (Y or N) " )
        if avocado == "Y" or avocado == "y":
            price += 0.75
            AVOCADO_COUNT += 1
        elif avocado == "N" or avocado == "N":
            price = price
        chili = input("Would you like chili? (Y or N) ")
        if chili == "Y" or chili == "y":
            price += 2.50
            CHILI_COUNT += 1
        elif chili == "N" or chili == "n":
            price = price
    side_order= input("Would you like Fries(F) or Rings(R)? or N ")
    if side_order == "F" or side_order == "f":
        price += 2.00
        FRIES_COUNT += 1
    elif side_order == "R" or side_order == "r":
        price += 2.25
        RINGS_COUNT += 1
    elif side_order == "N" or side_order == "n":
        price = price
    
    print("Order Summary")
    print("--------------")
    if BEEF_COUNT > 0:
        print(BEEF_COUNT, "Beef")
        
    if BEYOND_BEEF_COUNT > 0:
        print(BEYOND_BEEF_COUNT, "Beyond Beef")
    
    if DOUBLE_COUNT > 0:
        print(DOUBLE_COUNT, "Double")
    
    if TRIPLE_COUNT > 0:
        print(TRIPLE_COUNT, "Triple")
    
    if CHEESE_COUNT > 0:
        print(CHEESE_COUNT, "Cheese")
    
    if BACON_COUNT > 0:
        print(BACON_COUNT, "Bacon")
    
    if AVOCADO_COUNT > 0:
        print(AVOCADO_COUNT, "Avocado")
    
    if CHILI_COUNT > 0:
        print(CHILI_COUNT, "Chili")
    
    if FRIES_COUNT > 0:
        print(FRIES_COUNT, "Fries")
    
    if RINGS_COUNT > 0:
        print(RINGS_COUNT, "Onion Rings")

    print("Order Total: ${:.2f}".format(price)) 

    quit_statement = input("Press enter to continue, Q to quit ")
    if quit_statement == "":
        pass
    elif quit_statement == "Q" or quit_statement == "q":
        break

# Produce Sales Report
if quit_statement == "Q" or quit_statement == "q":
    for i in range (0, 1):
        print(2 * " " + "*" + 46 * " " + "*")
        print(1 * " " + "**" + 46 * " " + "**")
        print("***" + 46 * " " + "***")
        print(20 * "=" + "Sales Report" + 20 * "=")
        print("***" + 46 * " " + "***")
        print(1 * " " + "**" + 46 * " " + "**")
        print(2 * " " + "*" + 46 * " " + "*")
    print("\n")

print("Type" + 29 * " " + "Count" + 9 * " " + "Total")
print("Beef" + 32 * " ", BEEF_COUNT, 8 * " " + "{:.2f}".format(BEEF_COUNT * 5.75))
print("Beyond Beef" + 25 * " ", BEYOND_BEEF_COUNT, 8 * " " + "{:.2f}".format(BEYOND_BEEF_COUNT * 6.50))
print("-" * 52)
print("Grand Total: " + 23 * " ", BEEF_COUNT + BEYOND_BEEF_COUNT, 8 * " " + "{:.2f}".format(((BEEF_COUNT * 5.75) + (BEYOND_BEEF_COUNT * 6.50))))
