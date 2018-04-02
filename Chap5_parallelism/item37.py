#!/usr/bin/env python
'''
* Brett Slatkin, 2014, "effective Python"
* Brett Slatkin's example code([GitHub](https://github.com/bslatkin/effectivepython))
* I modified the example code a bit to confirm my understanding.
* item36.py is written in Python 3.6

Use threads for blocing I/O, avoid for parallelism
* Python threads cannot run bytecode in parallel on multiple CPU cores
  because of the Global Interpreter Lock(GIL)
* Python threads are still useful despite the GIL because they provide
  an easy way to do multiple things at seemingly the same time
* Use Python threads to make multiple system calls in parallel. This allows you
  to do blocking I/O at the same time as computation
'''
from time import time
from threading import Thread
import select, socket

# A computationally intersive function
def factorize(number):
    """
    A naive number factorization algorithm
    """
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

# Using multiple threads to do this computation
class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))

# Creating the socket is specifically to support Windows. Windows can't do
# a select call with an empty list.
def slow_systemcall():
    """
    Asks the OS system to block for 0.1 seconds
    """
    select.select([socket.socket()], [], [], 0.1)

# work to calculate the next helicopter move
# before waiting for the system call threads to finish
def compute_helicopter_location(index):
    print("computing helicopter location: {}".format(index))

if __name__=="__main__":
    print("A computationally intensive function..")
    numbers = [2139079, 1214759, 1516637, 1852285]
    start = time()
    for number in numbers:
        list(factorize(number))
    end = time()
    print('Took %.3f seconds' % (end - start))
    print("")

    print("Using multiple threads to do this computation")
    # start a thread for factorizing each number in parallel
    start = time()
    threads = []
    for number in numbers:
        thread = FactorizeThread(number)
        thread.start()
        threads.append(thread)

    # wait for all of the threads to finish
    for thread in threads:
        thread.join()
    end = time()
    print('Took %.3f seconds' % (end - start))
    print("This takes even longer....")
    print("")

    print("blocking I/O example")
    start = time()
    for _ in range(5):
        print("call slow_systemcall()")
        slow_systemcall()
    end = time()
    print('Took %.3f seconds' % (end - start))
    print("")

    print("run multiple invocatoins of the slow_systemcall in separate threads")
    start = time()
    threads = []
    for _ in range(5):
        thread = Thread(target=slow_systemcall)
        thread.start()
        threads.append(thread)

    # With the threads started, do some work
    for i in range(5):
        compute_helicopter_location(i)

    for thread in threads:
        thread.join()
    end = time()
    print('Took %.3f seconds' % (end - start))
    print("the parallel time is 5x times less than the serial time")
    print("""GIL prevents the Python code from running in parallel,
             but it has no negative effect on system calls""")
