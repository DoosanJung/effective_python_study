#!/usr/bin/env Python
'''
Problem: Python only allows for the single constructor method __init__
Solution: Use @classmethod polymorphism to construct objects generically
'''
import os
from threading import Thread
from item24_wrapper import TemporaryDirectory
from item24_not_good import execute, write_test_files
import random

class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        '''
        :param config: a dictionary with a set of configuration parameters
        '''
        raise NotImplementedError

class PathInputData(GenericInputData):
    def __init__(self, path):
        super(PathInputData, self).__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config = config):
            workers.append(cls(input_data))
        return workers

class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result

def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class = input_class, config = config)
    return execute(workers)

if __name__=="__main__":
    print("Use @classmethod polymorphism to construct objects generically")
    with TemporaryDirectory() as tmpdir:
        write_test_files(tmpdir)
        config = {'data_dir': tmpdir}
        result = mapreduce(worker_class = LineCountWorker, \
                        input_class = PathInputData, \
                        config = config)

    print('There are', result, 'lines')
