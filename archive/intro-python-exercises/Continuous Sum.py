theSum = 0
value = input("Enter a value to sum or press Enter to quit: ")

while value != "":
    number = int(value)
    theSum += number
    value = input("Enter a value to sum or press Enter to quit: ")
    if value == "":
        break
    else:
        continue

print("The sum is", theSum)