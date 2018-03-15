#!/usr/bin/env Python
'''
* Brett Slatkin, 2014, "effective Python"
* Brett Slatkin's example code([GitHub](https://github.com/bslatkin/effectivepython))
* I modified the example code a bit to confirm my understanding.

Problem: Python only allows for the single constructor method __init__
Solution: Use @classmethod polymorphism to construct objects generically
'''
import os
import sys
import random
from threading import Thread
from item24_wrapper import TemporaryDirectory
sys.dont_write_bytecode = True

# common class to represent the input data
class InputData(object):
    def read(self): # this method must be defined by subclasses
        raise NotImplementedError

class PathInputData(InputData):
    def __init__(self, path):
        # The no-argument syntax is specific to Python 3
        # So I pass in the class object and instance explicitly
        super(PathInputData, self).__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

# MapReduce worker: line counter
class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self): # this method must be defined by subclasses
        raise NotImplementedError

    def reduce(self, other): # this method must be defined by subclasses
        raise NotImplementedError

class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result

# manually build and connect the objects with some helper functions
def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name)) # a PathInputData instance

def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data)) # a LineCountWorker instance
    return workers

def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result

def mapreduce(data_dir): # connecting all three functiions
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

def write_test_files(tmpdir):
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(0, 100))

if __name__=="__main__":
    print("manually build and connect the objects with some helper functions")
    with TemporaryDirectory() as tmpdir:
        write_test_files(tmpdir = tmpdir)
        result = mapreduce(data_dir = tmpdir)

    print('There are', result, 'lines')
