# Desc: Calculates the first 10 fib numbers and prints them 

def fib(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return fib(x-1) + fib(x-2)
        
for foo in range (10):
    print fib(foo)