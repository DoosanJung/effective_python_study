#!/usr/bin/env Python
"""
'contextlib' and 'with' for reusable 'try/finally' behavior

Useful for enforcing semantics, debugging, registering functinos, etc..
"""
from threading import Lock
import logging
from contextlib import contextmanager

class LockExample(object):
    @staticmethod
    def lock_with(): # good
        '''
        better than 'try/finally'
        indented code only runs while the lock is held
        '''
        lock = Lock()
        with lock:
            print('Lock is held')

    @staticmethod
    def lock_try_finally(): # not good
        '''
        same as above
        worse than 'with'
        '''
        lock = Lock()
        lock.acquire()
        try:
            print('Lock is held')
        finally:
            lock.release()

class LoggingExample(object):

    logging.getLogger().setLevel(logging.WARNING)

    @staticmethod
    def my_function():
        '''
        since setLevel(logging.WARNING)
        my_function will only log "Error log here"
        '''
        logging.debug('Some debug data')
        logging.error('Error log here')
        logging.debug('More debug data')

    @staticmethod
    @contextmanager
    def debug_logging(level):
        '''
        elevate the log level of this function temporarily
        by defining a context manager
        '''
        logger = logging.getLogger()
        old_level = logger.getEffectiveLevel()
        logger.setLevel(level)
        try:
            yield # see item40.py
        finally:
            logger.setLevel(old_level)

    @classmethod
    def test_contextmanger(cls):
        '''
        call the same my_function(), but in the debug_logging context
        '''
        with cls.debug_logging(logging.DEBUG): # set to debug
            print('Inside:')
            cls.my_function()
        print('After:')
        cls.my_function() # using old_level

class UsingWithTargetsExample(object):
    '''
    (with ... as ...)

    The code (running in the with block) can directly interact
    with its context

    Example:
    with open('my_output.txt', 'w') as f:
        f.write('This is some data!')
    '''
    @staticmethod
    @contextmanager
    def log_level(level, name):
        logger = logging.getLogger(name)
        old_level = logger.getEffectiveLevel()
        logger.setLevel(level)
        try:
            yield logger # it can return an object!
        finally:
            logger.setLevel(old_level)

    @classmethod
    def test_with_as_example(cls):
        with cls.log_level(logging.DEBUG, 'my-log') as logger:
            logger.debug('This is my message!') # inside with ... as ...
            logging.debug('This will not print')

        # After the with statement exits, calling "my-log" does nothing
        # because the default logging severity level has been restored
        logger = logging.getLogger('my-log')
        logger.debug('Debug will not print')
        logger.error('Error will print')

if __name__=="__main__":
    LockExample.lock_with() # good
    LockExample.lock_try_finally() # not good
    print(" ")

    LoggingExample.my_function() # base
    LoggingExample.test_contextmanger() # using contextmanager
    print(" ")

    UsingWithTargetsExample.test_with_as_example() # with ... as ...
