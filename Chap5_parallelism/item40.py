#!/usr/bin/env python
'''
* Brett Slatkin, 2014, "effective Python"
* Brett Slatkin's example code([GitHub](https://github.com/bslatkin/effectivepython))
* I modified the example code a bit to confirm my understanding.
* item36.py is written in Python 3.6

Consider coroutines to run many functions concurrently
* Problems with Threads:
    (1) Difficult to extend and maintain
    (2) Threads require a lot of memory
    (3) Costly to start

* Use coroutines !!

* Python 2 does not support
    (1) "yield from"
    (2) returning values from generators
'''
from collections import namedtuple

def my_coroutine():
    """
    consuming a generator to send a value back into the generator
    after each yield expression
    """
    while True:
        received = yield
        print('Received:', received)

def minimize():
    """
    a generator coroutines that yields the minimum value it's benn sent so far
    """
    current = yield
    while True:
        value = yield current
        current = min(value, current)

#
# Conway's the game of life
#
def count_neighbors(y, x):
    """
    a coroutine:
        Sees the neighbor's states and returns the count of living neighbors
        yields Query for each neighbor
    """
    n_ = yield Query(y + 1, x + 0)  # North
    ne = yield Query(y + 1, x + 1)  # Northeast
    # Define e_, se, s_, sw, w_, nw ...
    e_ = yield Query(y + 0, x + 1)  # East
    se = yield Query(y - 1, x + 1)  # Southeast
    s_ = yield Query(y - 1, x + 0)  # South
    sw = yield Query(y - 1, x - 1)  # Southwest
    w_ = yield Query(y + 0, x - 1)  # West
    nw = yield Query(y + 1, x - 1)  # Northwest
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count

def step_cell(y, x):
    """
    a coroutine:
        receives its coordinates in the grid as arguments
        yields a Query to ge the initial state of those coordinates
        uses count_neighbors to inspect the cells around it
        runs game_logic to determine what state the cell should have for next tick
        yields Transition objects

    "yield from" statements:
        compose generator coroutines together;
        allow us to build complex coroutines from simpler ones
    """
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY     # Die: Too few
        elif neighbors > 3:
            return EMPTY     # Die: Too many
    else:
        if neighbors == 3:
            return ALIVE     # Regenerate
    return state

def simulate(height, width):
    """
    a coroutine:
        progresses the grid of cells forward by yielding from step_cell many times
        after progressing every coordinate, it yields TICK object to indicate that
        the current generation of cells have all transitioned.
        Each cell will transition by running step_cell
    """
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK

class Grid(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        output = ''
        for row in self.rows:
            for cell in row:
                output += cell
            output += '\n'
        return output

    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

def live_a_generation(grid, sim):
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:  # Must be a Transition
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny

class ColumnPrinter(object):
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(row_count, len(data.splitlines()) + 1)
        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line
                if (i + 1) < len(self.columns):
                    rows[j] += ' | '
        return '\n'.join(rows)

if __name__=="__main__":
    print("Using coroutines1: printing received value")
    it = my_coroutine()
    print("initial call to next(it) is required..")
    next(it)             # Prime the coroutine
    it.send('First')
    it.send('Second')
    print("")

    print("Using coroutines2: printing minimum value so far")
    it = minimize()
    print("initial call to next(it) is required..")
    next(it)            # Prime the generator
    print(it.send(10))
    print(it.send(4))
    print(it.send(22))
    print(it.send(-1))
    print("")

    print("""
    #
    # Conway's the game of life
    #
    """)
    ALIVE = '*'
    EMPTY = '-'
    Query = namedtuple('Query', ('y', 'x'))

    print("testing the count_neighbors functions with fake data")
    it = count_neighbors(10, 5)
    q1 = next(it)                  # Get the first query
    print('First yield: ', q1)
    q2 = it.send(ALIVE)            # Send q1 state, get q2
    print('Second yield:', q2)
    q3 = it.send(ALIVE)            # Send q2 state, get q3
    print('...')
    q4 = it.send(EMPTY)
    q5 = it.send(EMPTY)
    q6 = it.send(EMPTY)
    q7 = it.send(EMPTY)
    q8 = it.send(EMPTY)
    try:
        it.send(EMPTY)     # Send q8 state, retrieve count
    except StopIteration as e:
        print('Count: ', e.value)  # Value from return statement
    print("")

    Transition = namedtuple('Transition', ('y', 'x', 'state'))
    print("testing the step_cell functions with fake data")
    it = step_cell(10, 5)
    q0 = next(it)           # Initial location query
    print('Me:      ', q0)
    q1 = it.send(ALIVE)     # Send my status, get neighbor query
    print('Q1:      ', q1)
    print('...')
    q2 = it.send(ALIVE)
    q3 = it.send(ALIVE)
    q4 = it.send(ALIVE)
    q5 = it.send(ALIVE)
    q6 = it.send(EMPTY)
    q7 = it.send(EMPTY)
    q8 = it.send(EMPTY)
    t1 = it.send(EMPTY)     # Send for q8, get game decision
    print('Outcome: ', t1)
    print("")

    TICK = object()
    print("testing the grid class")
    grid = Grid(5, 9)
    grid.assign(0, 3, ALIVE)
    grid.assign(1, 4, ALIVE)
    grid.assign(2, 2, ALIVE)
    grid.assign(2, 3, ALIVE)
    grid.assign(2, 4, ALIVE)
    print(grid)
    print("")

    print("progress the grid forward one generation at a time")
    columns = ColumnPrinter()
    sim = simulate(grid.height, grid.width)
    for i in range(5):
        columns.append(str(grid))
        grid = live_a_generation(grid, sim)

    print(columns)
    print("")
