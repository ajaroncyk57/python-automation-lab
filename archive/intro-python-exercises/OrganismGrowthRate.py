organisms = int(input("Enter the initial number of organisms: "))
rate_of_growth = float(input("Enter the rate of growth as a whole number: "))
growth_period = int(input("Enter the time (in hours) it takes to achieve Rate of Growth: "))

HOURS = 0

for i in range(growth_period):
    organisms *= rate_of_growth
    HOURS += 1
    if HOURS == growth_period:
        break
    else:
        continue
    
print("After", growth_period, "hours, there are ", organisms)
