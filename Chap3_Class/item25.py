#!/usr/bin/env python
'''
Initialize parent classes with super
'''

# 1. Old way to Initialize a parent classd
class MyBaseClass(object):
    def __init__(self, value):
        self.value = value

class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)

    def times_two(self):
        return self.value * 2

# A problem arises with multiple inheritance
class TimesTwo(object): # a parent class
    def __init__(self):
        self.value *= 2

class PlusFive(object):  # a parent class
    def __init__(self):
        self.value += 5

class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

class AnotherWay(MyBaseClass, PlusFive, TimesTwo): # an ordering is diff
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

# Another problem arises with diamond inheritance
# a diamond inheritance causes the common superclass's __init__ method to run
# multiple times
class TimesFive(MyBaseClass): # a child class
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5

class PlusTwo(MyBaseClass): # a child class
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2

class ThisWay(TimesFive, PlusTwo): # making a diamon inheritance
    # Second parent class's constructor, PlusTwo.__init__ causes self.value to be
    # reset back to 5 when MyBaseClass.__init__ gets called a second time
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)

# Good way
# Python 2.2 added the super built-in function and defined
# the method resolution order (MRO)
# depth-first, left-to-right order
class MyBaseClass(object):
    def __init__(self, value):
        self.value = value

class TimesFiveCorrect(MyBaseClass):
    def __init__(self, value):
        super(TimesFiveCorrect, self).__init__(value)
        self.value *= 5

class PlusTwoCorrect(MyBaseClass):
    def __init__(self, value):
        super(PlusTwoCorrect, self).__init__(value)
        self.value += 2

class GoodWay(TimesFiveCorrect, PlusTwoCorrect):
    def __init__(self, value):
        super(GoodWay, self).__init__(value)

if __name__=="__main__":
    # Python 2.7 does not allow 1 ~ 3..
    # Python 2.7 also have not defined __class__
    # cannot use super(__class__, self).__init__(...)
    # or super().__init__(...)
    '''
    print("1. Old way to Initialize a parent class")
    foo = MyChildClass()
    print(foo.times_two())
    print("")

    print("2. A problem arises with multiple inheritance")
    foo = OneWay(5)
    print('First ordering is (5 * 2) + 5 =', foo.value)
    bar = AnotherWay(5)
    print('Second ordering still is', bar.value)
    print("It should be (5 + 5) * 2 = 20")
    print("")

    print("3. Another problem arises with diamond inheritance")
    foo = ThisWay(5)
    print('Should be (5 * 5) + 2 = 27 but is', foo.value)
    print("showing unexpected behaviors")
    print("")
    '''

    print("4. good way")
    good = GoodWay(5)
    print("Should be 5 * (5 + 2) = 35 and is", good.value)
    print("not 27")
    print("let's print method resolution ordering (MRO)")
    from pprint import pprint
    pprint(GoodWay.mro())
