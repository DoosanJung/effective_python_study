#!/usr/bin/env python
"""
make 'pickle' reliable with 'copyreg'
pickle can serialize Python objects into a stream of bytes

pickle module's serialization format is unsafe:
json module is safe:

'copyreg' allows you to control the behavior of pickle
"""
import pickle
import copy_reg

def base_game_state():
    state = GameState()
    state.level += 1  # Player beat a level
    state.lives -= 1  # Player had to try again

    # pickling
    state_path = 'game_state.bin'
    with open(state_path, 'wb') as f:
        pickle.dump(state, f) # dump the GameState directly

    # unpickling
    with open(state_path, 'rb') as f:
        state_after = pickle.load(f)
    print(state_after.__dict__)

def field_added_state():
    state = GameState()
    serialized = pickle.dumps(state)
    state_after = pickle.loads(serialized)
    print("field added GameState object")
    print(state_after.__dict__) # O.K
    print(" ")

    print("unpickling older saved GameState object..")
    state_path = 'game_state.bin' # older saved GameState object
    with open(state_path, 'rb') as f:
        state_after = pickle.load(f)
    print(state_after.__dict__) # O.K
    print("the points attribute is missing!")

# Solutino 1: put default attribute values
def default_attribute_values():
    print("using copy_reg")
    copy_reg.pickle(GameState, pickle_game_state)

    state = GameState()
    state.points += 1000

    # pickling
    serialized = pickle.dumps(state)

    # unpickling
    state_after = pickle.loads(serialized)
    print(state_after.__dict__)

    return serialized

def pickle_game_state(game_state):
    '''
    Takes a GameState object and turns it into
    a tuple of parameters
    '''
    kwargs = game_state.__dict__ # pass dictionary to kwargs
    return unpickle_game_state, (kwargs,)

def unpickle_game_state(kwargs):
    '''
    Takes serialized data and parameters from pickle_game_state
    returns the correspoding GameState object
    '''
    return GameState(**kwargs)

def default_attribute_values_add_field(serialized):
    state_after = pickle.loads(serialized)
    print(state_after.__dict__)

def default_attribute_values_rm_field(serialized):
    try:
        pickle.loads(serialized)
    except:
        print('Expected error')

def versioning_classes(serialized):
    copy_reg.pickle(GameState, pickle_game_state)
    state_after = pickle.loads(serialized)
    print(state_after.__dict__)

if __name__=="__main__":
    # base
    class GameState(object):
        def __init__(self):
            self.level = 0
            self.lives = 4

    print("base class")
    base_game_state()
    print(" ")

    # field added
    del GameState
    class GameState(object):
        def __init__(self):
            self.level = 0
            self.lives = 4
            self.points = 0

    # unpickling older saved GameState object..
    field_added_state()
    # "the points attribute is missing!"
    print(" ")

    print("Solution 1: Default attribute values")
    print("=="*30)
    # well, not Good
    # removing fields is not allowed...
    # e.g. removing 'lives' will cause an error when deserializing old game data
    del GameState
    class GameState(object):
        '''
        Use a constructor with default arguments

        To ensure the GameState objects will always have
        all attributes after unpickling
        '''
        def __init__(self, level=0, lives=4, points=0):
            self.level = level
            self.lives = lives
            self.points = points

    serialized = default_attribute_values()
    print("Use a constructor with default arguments works")
    print(" ")

    del GameState
    class GameState(object):
        """
        adding a field will still work
        """
        def __init__(self, level=0, lives=4, points=0, magic=5):
            self.level = level
            self.lives = lives
            self.points = points
            self.magic = magic

    default_attribute_values_add_field(serialized)
    print("adding a field will still work")
    print(" ")

    del GameState
    class GameState(object):
        def __init__(self, level=0, points=0, magic=5):
            """
            removing a field will break
            """
            self.level = level
            self.points = points
            self.magic = magic

    default_attribute_values_rm_field(serialized)
    print("removing a field will break Solution 1")
    print(" ")

    print("Solution2: Versioning Classes")
    print("=="*30)

    del pickle_game_state
    def pickle_game_state(game_state):
        kwargs = game_state.__dict__
        kwargs['version'] = 2
        return unpickle_game_state, (kwargs,)

    del unpickle_game_state
    def unpickle_game_state(kwargs):
        version = kwargs.pop('version', 1)
        if version == 1:
            kwargs.pop('lives')
        return GameState(**kwargs)

    versioning_classes(serialized)
    print("deserializing an old object works")


    # Stable import paths
    # pickle is breakage from renaming a class
    # Because the import path of the serialized object's class is encoded in the pickled data
    # Solution: copyreg.pickle(BetterGameState, pickle_game_state)
