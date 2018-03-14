#!/usr/bin/env python
"""
Generators: Generators are iterators, but you can only iterate over them once
Iterable: any object in Python which has an __iter__ or a __getitem__ method defined
        which returns an iterator or can take indexes")
Iterator: any object in Python which has a next (Python2) or __next__ method defined
"""

def generator_function(n):
    """
    does not store all the values in memory, generates the value on the fly
    """
    for i in range(n):
        yield i

# generator version
def fibon(n):
    a = 0; b = 1
    for i in range(n+1):
        yield a
        a, b = b, a + b

def next_func():
    """
    A built-in function, next, allows us to access the next element of a sequence.
    """
    gen = generator_function(3)
    print(next(gen))
    # Output: 0
    print(next(gen))
    # Output: 1
    print(next(gen))
    # Output: 2
    try:
        print(next(gen))
    except StopIteration:
        print("StopIteration")

def iter_func(my_string):
    """
    A built-in function, iter, returns an iterator object from an iterable

    'str' is an iterable but not an iterator
    next(my_string) will break
    """
    my_iter = iter(my_string)
    print(next(my_iter))
    # Output: Y
    print(next(my_iter))
    # Output: a
    print(next(my_iter))
    # Output: s
    print(next(my_iter))
    # Output: o
    print(next(my_iter))
    # Output: o
    print(next(my_iter))
    # Output: b
    try:
        print(next(my_iter))
    except StopIteration:
        print("StopIteration")

if __name__=="__main__":
    for item in generator_function(10):
        print("item in generator_function: ", item)

    print("using generator version of fibonacci")
    for x in fibon(10):
        print(x)

    print("using next(gen)")
    next_func()

    print("using iter(my_string)")
    my_string = "Yasoob"
    iter_func(my_string)
