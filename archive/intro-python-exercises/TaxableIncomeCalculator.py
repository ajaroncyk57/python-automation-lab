# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 00:26:13 2019

@author: Andrew Jaroncyk
"""

income = int(input("Enter how much you make: "))
taxable_income = 0.00

if 0 < income < 9700:
    taxable_income = income * 0.10
elif 9701 < income < 39475:
    taxable_income = income * 0.12
elif 39476 < income < 84200: 
    taxable_income = income * 0.22
elif 84201 < income < 160725: 
    taxable_income = income * 0.24
elif 160726 < income < 204100: 
    taxable_income = income * 0.32
elif 204101 < income < 510300:
    taxable_income = income * 0.35
else:
    print("Congrats, you make too much to be taxed!")
    
print("You owe ${:,.2f}".format(taxable_income), "in taxes")
