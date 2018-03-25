#!/usr/bin/env python
'''
* Brett Slatkin, 2014, "effective Python"
* Brett Slatkin's example code([GitHub](https://github.com/bslatkin/effectivepython))
* I modified the example code a bit to confirm my understanding.

Use
	__getattr__: called every time an attribute cannot be found in an object's instance dict.
	__getattribute__
	__setattr__
for lazy attributes
'''

class LazyDB(object):
	def __init__(self):
		self.exists = 5

	def __getattr__(self, name):
		value = "value for {}".format(name)
		setattr(self, name, value) # populates foo in the instance dict
		return value

class LoggingLazyDB(LazyDB):
	def __getattr__(self, name):
		print("**** Called __getattr__(%s) ****" % name)
		return super(LoggingLazyDB, self).__getattr__(name)

class ValidatingDB(object):
	def __init__(self):
		self.exists = 5

	def __getattribute__(self, name):
		# called every time an attribute is accessed on an object
		# even in the cases where it does not exist in the attribute dict.
		print("**** Called __getattribute__(%s) ****" % name)
		try:
			return super(ValidatingDB, self)._-__getattribute__(name)
		except AttributeError:
			value = "Value for %s" % name
			setattr(self, name, value)
			return value

class MissingPropertyDB(object):
    def __getattr__(self, name):
		# if a dynamically accessed property should not exist,
		# raise an AttributeError
        if name == 'bad_name':
            raise AttributeError('%s is missing' % name)
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value

class SavingDB(object):
    def __setattr__(self, name, value):
        # Save some data to the DB log
		# called every time an attribute is assigned on an instance
        super(SavingDB, self).__setattr__(name, value)

class LoggingSavingDB(SavingDB):
    def __setattr__(self, name, value):
        print('Called __setattr__(%s, %r)' % (name, value))
        super(LoggingSavingDB, self).__setattr__(name, value)

class BrokenDictionaryDB(object):
    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
		print('Called __getattribute__(%s)' % name)
		# this requires accessing self._data from the __getattribute__ method
		# However, Python will recurse and it will die

		# __getattribute__ accesses self._data
		# _self.data causes __getattribute__ to run again
		# __getattribute__ accesses self._data again
		# ...
		return self._data[name]

class DictionaryDB(object):
	def __init__(self, data):
		self._data = data

	def __getattribute__(self, name):
		data_dict = super(DictionaryDB, self).__getattribute__('_data')
		return data_dict[name]

if __name__=="__main__":
	data = LazyDB()
	print("Before: ", data.__dict__)
	print("foo:    ", data.foo)
	print("foo attributes is not in the instance dict initiallys")
	print("After:  ", data.__dict__)
	print(" ")

	data = LoggingLazyDB()
	print("exists:     ", data.exists)
	print("Before:     ", data.__dict__)
	print("foo exists: ", hasattr(data, 'foo'))
	print("foo:        ", data.foo)
	print("foo exists: ", hasattr(data, 'foo'))
	print("foo attributes is not in the instance dict initiallys")
	print("foo:        ", data.foo)
	print("__getattr__ has setattr so __getattr__ did not called in 2nd time")
	print(" ")

	data = ValidatingDB()
	print("exists: ", data.exists)
	print("foo:    ", data.foo)
	print("foo:    ", data.foo)
	print(" ")

	data = MissingPropertyDB()
	print("foo:    ", data.foo)
	try:
		print("foo:    ", data.bad_name)
	except:
		print("AttributeError Expected")
	print(" ")

	data = LoggingSavingDB()
	print('Before: ', data.__dict__)
	data.foo = 5
	print('After:  ', data.__dict__)
	data.foo = 7
	print('Finally:', data.__dict__)
	print(" ")

	try:
	    data = BrokenDictionaryDB({'foo': 3})
	    data.foo
	except:
	    print('using BrokenDictionaryDB: RunTimeError Expected')
	else:
	    assert False
	print(" ")

	print("using DictionaryDB: solved recusrion problem")
	data = DictionaryDB({'foo': 3})
	print(data.foo)
