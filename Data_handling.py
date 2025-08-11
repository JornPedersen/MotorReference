
#Make a list on where to split the big data array
def split_id(data):

    split_arr = []
    old_data = data[0]
    split_arr.append(1)


    for i in range(0, (data.size)):
        if old_data - data[i] > 1:
            split_arr.append(i+1)
            old_data = data[i]
        else:
            old_data = data[i]
    
    split_arr.append(data.size + 1)

    return(split_arr)