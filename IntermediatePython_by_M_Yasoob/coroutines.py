#!/usr/bin/env python
"""
Coroutines are similar to generators with a few differences
* generators are data producers
* coroutines are data consumers: It does not contain any value initially,
                                instead we supply it values externally
"""

def grep(pattern):
    print ("Searching for %s" % pattern)
    while True:
        line = (yield) # a coroutine
        if pattern in line:
            print(line)

def using_coroutines():
    search = grep('Python')
    print("using next() to start the coroutine..")
    next(search) # next is required in order to start the coroutine
    # Output: Searching for Python
    print(" ")
    search.send("I love you")
    search.send("Don't you love me?")
    search.send("I love Python instead!")
    # Output: I love Python instead!
    search.close()






if __name__=="__main__":
    using_coroutines()
