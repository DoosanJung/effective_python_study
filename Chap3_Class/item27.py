#!/usr/bin/env python
'''
* Brett Slatkin, 2014, "effective Python"
* Brett Slatkin's example code([GitHub](https://github.com/bslatkin/effectivepython))
* I modified the example code a bit to confirm my understanding.

Prefer public attributes over private ones
'''
class MyObject(object):
    def __init__(self):
        self.public_field = "public_field"
        self.__private_field = "__private_field1"

    def get_private_field(self):
        return self.__private_field

class MyOtherObject(object):
    def __init__(self):
        self.__private_field = "__private_field2"

    @classmethod
    def get_private_field(cls, instance):
        return instance.__private_field

# A subclass cannot access its parent's private fields
class MyParentObject(object):
    def __init__(self):
        self.__private_field = "parent__private_field"

class MyChildObject(MyParentObject):
    def get_private_field(self):
        """
        try to access its parent's private field
        """
        return self.__private_field

# Bad approach: using private fields in parent class
# A subclass can access to its parent's private field
class MyClass(object):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)

class MyIntegerSubclass(MyClass):
    def get_value(self):
        """
        subclass overrides..
        potentailly break stuffs..
        """
        return int(self._MyClass__value)

# If the class hierarchy changes..
class MyBaseClass(object):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

class MyNewClass(MyBaseClass):
    def get_value(self):
        return str(super().get_value())

class MyNewIntegerSubclass(MyNewClass):
    def get_value(self):
        return int(self._MyClass__value)

# Good approach: using protected attributes
# Document each protected field and explain
# which are internal APIs available to subclasses and
# which should be left alone entirely.
"""
class MyClass(object):
    def __init__(self, value):
        # This stores the user-supplied value for the object.
        # It should be coercible to a string. Once assigned for
        # the object it should be treated as immutable.
        self._value = value

    def get_value(self):
        return str(self._value)

class MyIntegerSubclass(MyClass):
    def get_value(self):
        return self._value
"""

# The only time to seriously consider using private attributes is
# naming conflicts with subclasses
class ApiConflictClass(object):
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value

class ChildConflict(ApiConflictClass):
    def __init__(self):
        super(ChildConflict, self).__init__()
        self._value = 'hello'  # Conflicts

# Using private attributes can fix this.
class ApiClass(object):
    def __init__(self):
        self.__value = 5

    def get(self):
        return self.__value

class Child(ApiClass):
    def __init__(self):
        super(Child, self).__init__()
        self._value = 'hello'  # OK!


if __name__=="__main__":
    print("get_private_field method works")
    my_obj = MyObject()
    get_private =  my_obj.get_private_field()
    print get_private
    print(" ")

    print("directly accessig private field raises an exception")
    try:
        print(my_obj.__private_field)
    except AttributeError:
        print("AttributeError!!")
    print(" ")

    print("Class methods also have access to private attributes")
    my_other_obj = MyOtherObject()
    get_private =  MyOtherObject.get_private_field(my_other_obj)
    print get_private
    print(" ")

    print("A subclass cannot access its parent class's private fields")
    my_child_obj = MyChildObject()
    try:
        print(my_child_obj.get_private_field())
    except AttributeError:
        print("AttributeError!!")

    print("The real name is..")
    print("my_child_obj._MyParentObject__private_field")
    print(my_child_obj._MyParentObject__private_field)
    print(" ")

    print("Bad approach: using private attributes in parents class")
    my_class = MyClass(5)
    print("my_class.get_value()")
    print(type(my_class.get_value()))
    print("my_integer_subclass.get_value()")
    my_integer_subclass = MyIntegerSubclass(5)
    print(type(my_integer_subclass.get_value()))
    print("A subclass can still access to its parent's private field... Bad!!")

    print("If the class hierarchy changes, it breaks..")
    try:
        my_new_integer_subclass = MyNewIntegerSubclass(5)
        my_new_integer_subclass.get_value()
    except:
        print("my_new_integer_subclass.get_value() throws AttributeError")
    print(" ")

    print("Good approach: using protected attributes and docstring")
    print("""
        class MyClass(object):
            def __init__(self, value):
                # This stores the user-supplied value for the object.
                # It should be coercible to a string. Once assigned for
                # the object it should be treated as immutable.
                self._value = value

            def get_value(self):
                return str(self._value)

        class MyIntegerSubclass(MyClass):
            def get_value(self):
                return self._value
    """)

    print("Using protected attributes: naming conflicts with subclasses")
    child_confilict = ChildConflict()
    print(child_confilict.get(), 'and', child_confilict._value, 'should be different')
    print("Using private attributes in Parent Class can fix this.")
    child = Child()
    print(child.get(), 'and', child ._value, 'are different')
