# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 12:13:32 2019

@author: Andrew Jaroncyk
"""
import random

print("Welcome to the dice rolling simulator")
print("Get ready to roll dem bones!")
simulation = int(input("How many roles should we simulate?\n\n"))
print("Simulation Outcome:")
print("-------------------")
total2 = ""
total3 = ""
total4 = ""
total5 = ""
total6 = ""
total7 = ""
total8 = ""
total9 = ""
total10 = ""
total11 = ""
total12 = ""

for i in range(0, simulation):
    roll = random.randint(1,6) + random.randint(1,6)
    if roll  == 2:
        total2 += "|"
    elif roll == 3:
        total3 += "|"
    elif roll == 4:
        total4 += "|"
    elif roll == 5:
        total5 += "|"
    elif roll == 6:
        total6 += "|"
    elif roll == 7:
        total7 += "|"
    elif roll == 8:
        total8 += "|"
    elif roll == 9:
        total9 += "|"
    elif roll == 10:
        total10 += "|"
    elif roll == 11:
        total11 += "|"
    elif roll == 12:
        total12 += "|"

print("{:10}".format("Twos:"), total2)
print("{:10}".format("Threes:"), total3)
print("{:10}".format("Fours:"), total4)
print("{:10}".format("Fives:"), total5)
print("{:10}".format("Sixes:"), total6)
print("{:10}".format("Sevens:"), total7)
print("{:10}".format("Eights:"), total8)
print("{:10}".format("Nines:"), total9)
print("{:10}".format("Tens:"), total10)
print("{:10}".format("Elevens:"), total11)
print("{:10}".format("Twelves:"), total12)
