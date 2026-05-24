# Function that takse two integer values and returns True if 
# first is the multiple of second, that is n = m*i for some integer i, False otherwise
def is_multiple(n, m):
    if n < m:
        return False
    elif n==m:
        return True
    else:
        return is_multiple(n-m, m)
    
def is_multiple2(n,m):
    if(n % m == 0):
        return True
    else:
        return False
# Test cases
print(is_multiple(10, 5)) # True
print(is_multiple(10, 3)) # False
print(is_multiple(15, 5)) # True
print(is_multiple(15, 4)) # False
print(is_multiple(20, 5)) # True
print("Using the second function:")
print(is_multiple2(10, 5)) # True
print(is_multiple2(10, 3)) # False
print(is_multiple2(15, 5)) # True
print(is_multiple2(15, 4)) # False
print(is_multiple2(20, 5)) # True