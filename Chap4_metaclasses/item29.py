#!/usr/bin/env python
'''
* Brett Slatkin, 2014, "effective Python"
* Brett Slatkin's example code([GitHub](https://github.com/bslatkin/effectivepython))
* I modified the example code a bit to confirm my understanding.

Use plain attributes instead of get and set methods
'''
# explicit getter and setter methods: Not Pythonic.
class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms

# never need to implement explicit setter or getter
# just use public attributes
class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

# Use @property decorator if needed
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super(VoltageResistance, self).__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

# using @property decorator setter
# lets you perform type checking and validation on input
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super(BoundedResistance, self).__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms

# using @property to make attributes from parent classes immutable
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super(FixedResistance,self).__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms

# wrong usage: do not set other attributes in getter property methods
class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        self._ohms = ohms


if __name__=="__main__":
    print("# explicit getter and setter methods: Not Pythonic.")
    r0 = OldResistor(50e3)
    print('Before: %5r' % r0.get_ohms())
    r0.set_ohms(10e3)
    print('After:  %5r' % r0.get_ohms())
    print("getting clumsy..")
    print("r0.set_ohms(r0.get_ohms() + 5e3)")
    r0.set_ohms(r0.get_ohms() + 5e3)
    print('After:  %5r' % r0.get_ohms())
    print(" ")

    print("# just using public attributes suffices. And it is simple")
    r1 = Resistor(50e3)
    r1.ohms = 10e3
    print('ohms, volts, amps: ')
    print('%r ohms, %r volts, %r amps' %
          (r1.ohms, r1.voltage, r1.current))
    print("r1.ohms += 5e3")
    r1.ohms += 5e3
    print('After:  %5r' % r0.get_ohms())
    print(" ")

    print("# Use @property decorator if needed")
    print(
    """
    class Resistor(object):
        def __init__(self, ohms):
            self.ohms = ohms
            self.voltage = 0
            self.current = 0

    class VoltageResistance(Resistor):
        def __init__(self, ohms):
            super(VoltageResistance, self).__init__(ohms)
            self._voltage = 0

        @property
        def voltage(self):
            return self._voltage

        @voltage.setter
        def voltage(self, voltage):
            self._voltage = voltage
            self.current = self._voltage / self.ohms
    """
    )
    r2 = VoltageResistance(1e3)
    print('Before: %5r amps' % r2.current)
    print("assigning the voltage property will run the voltage setter method")
    print("r2.voltage = 10")
    r2.voltage = 10
    print('After:  %5r amps' % r2.current)
    print(" ")

    print(
    """# using @property decorator setter lets you perform type checking
    and validation on input"""
    )
    print(
    """
    class BoundedResistance(Resistor):
        def __init__(self, ohms):
            super(BoundedResistance, self).__init__(ohms)

        @property
        def ohms(self):
            return self._ohms

        @ohms.setter
        def ohms(self, ohms):
            if ohms <= 0:
                raise ValueError('%f ohms must be > 0' % ohms)
            self._ohms = ohms
    """
    )
    try:
        r3 = BoundedResistance(1e3)
        print("try to set ohms = 0..")
        r3.ohms = 0
    except:
        print('Error: Expected')
    print(" ")

    print("# error if you pass an invalid value to the constructor")
    print("Becuase BoundedResistance.__init__ calls Resistor.__init__ and")
    print("Resistor.__init__ assigns self.ohms = -5")
    try:
        print("try to pass -5 to BoundedResistance.__init__(self, ohms)")
        BoundedResistance(-5)
    except:
        print('Error: Expected')
    print(" ")

    print("# using @property to make attributes from parent classes immutable")
    print("# try to assgin property after construction raises an error")
    print(
    """
    class FixedResistance(Resistor):
        def __init__(self, ohms):
            super(FixedResistance,self).__init__(ohms)

        @property
        def ohms(self):
            return self._ohms

        @ohms.setter
        def ohms(self, ohms):
            if hasattr(self, '_ohms'):
                raise AttributeError("Can't set attribute")
            self._ohms = ohms
    """)
    try:
        r4 = FixedResistance(1e3)
        print("try to assgin property after construction")
        r4.ohms = 2e3
    except:
        print('Error: Expected')
    print(" ")

    print("# wrong usage: do not set other attributes in getter property methods")
    print(
    """
    class MysteriousResistor(Resistor):
        @property
        def ohms(self):
            self.voltage = self._ohms * self.current
            return self._ohms

        @ohms.setter
        def ohms(self, ohms):
            self._ohms = ohms
    """)
    r7 = MysteriousResistor(10) # setting r7.ohms = 10
    r7.current = 0.01 # setting other attributes
    print('Before: r7.voltage == %5r' % r7.voltage)
    r7.ohms # r7.ohms == 10
    print('After: r7.voltage ==  %5r' % r7.voltage) # Why...???
    print("Extremely bizzare behovior..")
