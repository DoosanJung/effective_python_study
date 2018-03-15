#!/usr/bin/env Python
'''
* Brett Slatkin, 2014, "effective Python"
* Brett Slatkin's example code([GitHub](https://github.com/bslatkin/effectivepython))
* I modified the example code a bit to confirm my understanding.

Accept functions for simple interfaces instead of classes.
Functions and methods can be pased around and refereced like any other value.
'''
from collections import defaultdict

## 1. first-class functions
def log_missing():
    print("Key added")
    return 0

## 2. defining a small class
class CountMissing(object):
    def __init__(self):
        self.added = 0

    def missing(self): # who calls this method??
        self.added += 1
        return 0

## 3. defining a better class
class BetterCountMissing(object):
    def __init__(self):
        self.added = 0

    def __call__(self): # special method
        self.added += 1
        return 0

if __name__=="__main__":
    ## 1. first-class functions
    print("Customizing the behavior of the defaultdict")
    current = {"green":12, "blue":3}
    increments = [
        ("red", 5),
        ("blue", 17),
        ("orange", 9)
    ]
    result = defaultdict(log_missing, current) #log_missing will be called each time a missing key is accessed
    print("before", dict(result))
    for key, amount in increments:
        result[key] += amount
    print("after", dict(result))
    print("")

    ## 2. defining a small class
    print("Can reference the CountMissing.missing method directly on an object")
    print("and pass it to defaultdict as the default value hook")
    counter = CountMissing()
    result = defaultdict(counter.missing, current) # method ref
    for key, amount in increments:
        result[key] += amount
    print("The number of key added: {}".format(counter.added))
    print("")
    assert counter.added == 2

    ## 3. defining a better class
    print("Not obvious what the purpose of the CountMissing class is")
    print("To clarify, Python allows you to define the __call__ special method")
    print("Method __call__ allows an object to be called just like a function")
    counter = BetterCountMissing()
    counter()
    assert callable(counter)

    counter = BetterCountMissing()
    result = defaultdict(counter, current)
    for key, amount in increments:
        result[key] += amount
    print("The number of key added: {}".format(counter.added))
    assert counter.added == 2
