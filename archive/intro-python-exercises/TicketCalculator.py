# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 20:03:25 2019

Author: Andrew Jaroncyk
Name: Automatic Ticket Price Tabulator
Purpose: Program that calculates the total cost of tickets purchased by a
customer for a theater performance. 

STATE_TAX = 0.0625 (6.25%)
CITY_TAX = 0.0075 (0.75%)
"""
STATE_TAX = 0.0625
CITY_TAX = 0.0075

print("Welcome to the Automatic Ticket Price Tabulator")

TicketPrice = float(input("Please enter ticket price level "))
TicketQuant = int(input("Please enter number of tickets: "))
        
print("Sale Report for Ticket Purpose")
print("------------------------------")

TicketCost = TicketPrice * TicketQuant
TicketCost = '%.2f' % TicketPrice
print("Ticket Cost:            " + str(TicketCost))

TicketCost = float(TicketCost)
StateTaxCost = float(TicketCost * STATE_TAX)
StateTaxCost2 = round(StateTaxCost, 2)
print("State Tax:                " + str(StateTaxCost2))

TicketCost = float(TicketCost)
CityTaxCost = float(TicketCost * CITY_TAX)
CityTaxCost2 = round(CityTaxCost, 2)
print("City Tax:                 "+ str(CityTaxCost2))

TotalCost = float(TicketCost + StateTaxCost + CityTaxCost)
TicketCost = '%.2f' % TotalCost
print("Total Cost:             "+ str(TotalCost))
