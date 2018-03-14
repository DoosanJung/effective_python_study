#!/usr/bin/env python
"""
*args and **kwargs
"""

def test_var_args(f_arg, *args):
    """
    *args is used to send a non-keyworded variable length argument list to the function
    """
    print("first normal arg:", f_arg)
    for arg in args:
        print("another arg through *args:", arg)

def greet_me(**kwargs):
    """
    **kwargs allows you to pass keyworded variable length of arguments to a function
    Use **kwargs if you want to handle named arguments in a function
    """
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            print("{0} = {1}".format(key, value))

if __name__=="__main__":
    print("args")
    test_var_args('yasoob', 'python', 'eggs', 'test')

    print("kwargs")
    greet_me(name="yasoob")
