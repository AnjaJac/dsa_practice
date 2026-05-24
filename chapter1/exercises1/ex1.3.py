# #function that takes a sequence of one or more numbers, and returns the largest and smallest number
#in the form of tuple of form (largest, smallest)
def minmax(data):
    if len(data) == 0:
        return None
    elif len(data) == 1:
        return (data[0], data[0])
    else:
        max_val = data[0]
        min_val = data[0]
        for num in data:
            if num > max_val:
                max_val = num
            elif num < min_val:
                min_val = num
        return (max_val, min_val)
# Test cases
print(minmax([3, 1, 4, 1, 5, 9])) # (9, 1)
print(minmax([-2, -1, 0, 1, 2])) # (2, -2)
print(minmax([42])) # (42, 42)
print(minmax([])) # None  
