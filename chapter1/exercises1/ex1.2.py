# Function that determines if the integer value is even or odd

def is_even(k):
   if k < 0:
      k = -k
   if k == 0:
        return True   
   elif k == 1:
        return False
   else:
        return is_even(k-2)
   

# Test cases
print(is_even(0)) # True
print(is_even(1)) # False
print(is_even(2)) # True
print(is_even(3)) # False
print(is_even(4)) # True
print(is_even(5)) # False
print(is_even(10)) # True
print(is_even(-144))