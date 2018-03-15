#!/usr/bin/env python
"""
* Brett Slatkin, 2014, "effective Python"
* Brett Slatkin's example code([GitHub](https://github.com/bslatkin/effectivepython))
* I modified the example code a bit to confirm my understanding.

Use built-in algorithms and data structures
"""
from collections import deque
from random import randint
from collections import OrderedDict
from collections import defaultdict
from heapq import *
from bisect import bisect_left
from timeit import timeit

def double_ended_queue():
    """
    deque provides constant time operations

    Inserting and removing items from the head of the 'list'
    takes linear time
    Inserting and removing items from the end of the 'list'
    takes constant time
    """
    fifo = deque()
    fifo.append(1); print("append 1");      # Producer
    fifo.append(2); print("append 2");
    fifo.append(3); print("append 3");
    x = fifo.popleft(); print("popleft");  # Consumer
    print(x)

def ordered_dict():
    print("standard dictionaries are unordered")
    a = OrderedDict()
    a['foo'] = 1; print("a = {foo: 1}");
    a['bar'] = 2; print("a = {foo: 1, bar: 2}");

    b = OrderedDict()
    b['foo'] = 'red'; print("b = {foo: red}");
    b['bar'] = 'blue'; print("b = {foo: red, bar: blue}");

    for value1, value2 in zip(a.values(), b.values()):
        print(value1, value2)

def default_dict():
    print("messy codes..")
    stats = {}
    key = 'my_counter'
    print("if key not in dictionary:...")
    if key not in stats:
        stats[key] = 0
    stats[key] += 1
    print(stats)

    print("storing a default vaule when a key does not exist")
    stats = defaultdict(int)
    stats['my_counter'] += 1
    print(dict(stats))

def heap_queue():
    print("heaps are useful for maintating a priority queue")
    a = []
    heappush(a, 5);print("heappush 5")
    heappush(a, 3);print("heappush 3")
    heappush(a, 7);print("heappush 7")
    heappush(a, 4);print("heappush 4")
    print(" ")

    print("removed by highest prioiry - lowest number - first")
    print("heappop! 4 times")
    print(heappop(a), heappop(a), heappop(a), heappop(a))
    print(" ")

    print("accessing the 0 index == the smallest item")
    a = []
    heappush(a, 5);print("heappush 5")
    heappush(a, 3);print("heappush 3")
    heappush(a, 7);print("heappush 7")
    heappush(a, 4);print("heappush 4")
    assert a[0] == nsmallest(1, a)[0] == 3

    # Example 9
    print('Before sorting:', a)
    a.sort()
    print('After sorting: ', a)

def bisection():
    print("searching for an item in a list takes linear time")
    print("proportional to its length ")
    x = list(range(10**6))
    i = x.index(991234)
    print(i)

    print("efficient binary search throught a sequence of sorted items")
    i = bisect_left(x, 991234)
    print(i)

    print(timeit(
        'a.index(len(a)-1)',
        'a = list(range(100))',
        number=10**6))
    print(timeit(
        'bisect_left(a, len(a)-1)',
        'from bisect import bisect_left;'
        'a = list(range(10**6))',
        number=10**))


if __name__=="__main__":
    print("..double_ended_queue")
    double_ended_queue()
    print(" ")

    print("..OrderedDict")
    ordered_dict()
    print(" ")

    print("..defaultdict")
    default_dict()
    print(" ")

    print("heap_queue")
    heap_queue()
    print(" ")

    print("bisection")
    bisection()
    print(" ")
