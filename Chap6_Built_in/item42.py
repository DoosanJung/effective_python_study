#!/usr/bin/env Python
'''
* Brett Slatkin, 2014, "effective Python"
* Brett Slatkin's example code([GitHub](https://github.com/bslatkin/effectivepython))
* I modified the example code a bit to confirm my understanding.

Define functino decorators with 'functools.wrap'
Decorators have the ability to run additional code before and after any calls
to the functions they wrap.

Useful for enforcing semantics, debugging, registering functinos, etc..
'''

# printing arguments and return value
# especially helpful for recursive functions
# however, this is not good..
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' %
              (func.__name__, args, kwargs, result))
        return result
    return wrapper

@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

# good!
from functools import wraps
# this will copy all of the important metadata about the inner function
# to outer function.

def trace_good(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' %
              (func.__name__, args, kwargs, result))
        return result
    return wrapper

@trace_good
def fibonacci_trace_good(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))


if __name__=="__main__":
    result = fibonacci(3) # O.K

    help(fibonacci) # O.K

    result_trace_good = fibonacci_trace_good(3) # O.K

    help(fibonacci_trace_good) # O.K

    # testing trace_good: O.K
    print("testing trace_good...")
    try:
        # Example of how pickle breaks
        import pickle

        def my_func():
            return 1

        # This will be okay
        print('pickle.dumps(my_func)',pickle.dumps(my_func))

        @trace_good
        def my_func2():
            return 2

        # This will not explode
        print('pickle.dumps(my_func2)', pickle.dumps(my_func2))
    except:
        print('Expected exception')
    print(" ")

    # testing trace: ERROR!!!!!!
    print("testing trace...")
    try:
        # Example of how pickle breaks
        import pickle

        def my_func():
            return 1

        # This will be okay
        print('pickle.dumps(my_func)',pickle.dumps(my_func))

        @trace
        def my_func2():
            return 2

        # This will explode
        print(pickle.dumps(my_func2))
    except:
        print('Expected exception!!!')
