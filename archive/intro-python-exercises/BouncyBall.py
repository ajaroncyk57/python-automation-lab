drop_height = int(input("Enter the height from which the ball was dropped: "))
bounce_height = int(input("Enter how hight the ball bounced on the first bounce: "))
bounce_index = bounce_height/drop_height

bounce = 1
height = drop_height
distance_initial = 0
distance_new = distance_initial

while drop_height >= 0:
    bounce += 1
    distance_initial = bounce_height + drop_height
    bounce_height *= bounce_index
    drop_height *= bounce_index
    distance_new = distance_initial + drop_height + bounce_height
    if bounce_height < 0:
        break
    break
    
print("Total Distance Traveled: {:.2f}".format(distance_new))
    

    
