# -*- coding: utf-8 -*- 
"""
--------------------------------------------------
File Name:        Chap4_Comprehensions_and_Generators
Description:    
Author:           jiaxuanliang
Date:             6/15/22
--------------------------------------------------
Change Activity:  6/15/22
--------------------------------------------------
"""

# Python provides a special syntax, called comprehensions,
# for succinctly iterating through these types and creating derivative data structures.
# This style of processing is extended to functions with generators,
# which enable a stream of values to be incrementally returned by a function.
# The result of a call to a generator function can be used
# anywhere an iterator is appropriate (e.g., for loops, starred expressions).
# Generators can improve performance, reduce memory usage, and increase readability.

# Item 27: Use Comprehensions Instead of map and filter
# Python provides compact syntax for deriving a new list from another sequence or iterable.
# These expressions are called list comprehensions.
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [x**2 for x in a]  # List comprehension
print(squares)

# List comprehensions let you easily filter items from the input list,
# removing corresponding outputs from the result.
even_squares = [x**2 for x in a if x % 2 == 0]
print(even_squares)

# The filter built-in function can be used along with map to achieve the same outcome,
# but it is much harder to read.
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)

# Dictionaries and sets have their own equivalents of list comprehensions
# (called dictionary comprehensions and set comprehensions, respectively).
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
threes_cubed_set = {x**3 for x in a if x % 3 == 0}
print(even_squares_dict)
print(threes_cubed_set)

alt_dict = dict(map(lambda x: (x, x**2),
                filter(lambda x: x % 2 == 0, a)))
alt_set = set(map(lambda x: x**3,
              filter(lambda x: x % 3 == 0, a)))

# Item 28: Avoid More Than Two Control Subexpressions in Comprehensions
# Beyond basic usage, comprehensions support multiple levels of looping.

# For example, say that I want to simplify a matrix (a list containing other list instances)
# into one flat list of all cells.
# This example is simple, readable, and a reasonable usage of multiple loops in a comprehension.
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]  # subexpressions run in the order provided, from left to right
print(flat)

# Another reasonable usage of multiple loops involves replicating the two-level-deep layout of the input list.
# This comprehension is noisier because of the extra [] characters, but it’s still relatively easy to read
squared = [[x**2 for x in row] for row in matrix]
print(squared)

# Using normal loop statements rather than the three-level-list comprehension.

# Comprehensions support multiple if conditions.
# Multiple conditions at the same loop level have an implicit and expression.
# to filter a list of numbers to only even values greater than 4
# These two list comprehensions are equivalent:
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0]

# Conditions can be specified at each level of looping after the for subexpression.
# Expressing this with a list comprehension does not require a lot of code,
# but it is extremely difficult to read.
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]
print(filtered)

# Although this example is a bit convoluted, in practice
# you’ll see situations arise where such comprehensions seem like a good fit.
# I strongly encourage you to avoid using list, dict, or set comprehensions that look like this.

# The rule of thumb is to avoid using more than two control subexpressions in a comprehension.
# This could be two conditions, two loops, or one condition and one loop.
# As soon as it gets more complicated than that,
# you should use normal if and for statements and write a helper function

# Item 29: Avoid Repeated Work in Comprehensions by Using Assignment Expressions
# A common pattern with comprehensions—including list, dict, and set variants
# —is the need to reference the same computation in multiple places.
stock = {
    'nails': 125,
    'screws': 35,
    'wingnuts': 8,
    'washers': 24,
}
order = ['screws', 'wingnuts', 'clips']


def get_batches(count, size):
    return count // size


result = {}
for name in order:
    count = stock.get(name, 0)
    batches = get_batches(count, 8)
    if batches:
        result[name] = batches
print(result)

# implement this looping logic more succinctly using a dictionary comprehension
found = {name: get_batches(stock.get(name, 0), 8)
         for name in order
         if get_batches(stock.get(name, 0), 8)}
print(found)

# to use the walrus operator (:=) to form an assignment expression
# as part of the comprehension
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}

# It’s valid syntax to define an assignment expression in the value expression for a comprehension.
# But if you try to reference the variable it defines in other parts of the comprehension,
# you might get an exception at runtime because of the order in which comprehensions are evaluated
# Error
result = {name: (tenth := count // 10)
          for name, count in stock.items() if tenth > 0}

# Fix
result = {name: tenth for name, count in stock.items()
          if (tenth := count // 10) > 0}
print(result)

# If a comprehension uses the walrus operator in the value part of the comprehension
# and doesn’t have a condition, it’ll leak the loop variable into the containing scope
half = [(last := count // 2) for count in stock.values()]
print(f'Last item of {half} is {last}')
# (doubt: in this case, count is not defined, so count didn't leak)

# This leakage of the loop variable is similar to what happens with a normal for loop
for count in stock.values():  # Leaks loop variable
    pass
print(f'Last item of {list(stock.values())} is {count}')

# However, similar leakage doesn’t happen for the loop variables from comprehensions
half = [count // 2 for count in stock.values()]
print(half)   # Works
print(count)  # Exception because loop variable didn't leak

# Using an assignment expression also works the same way in generator expressions
found = ((name, batches) for name in order
         if (batches := get_batches(stock.get(name, 0), 8)))
print(next(found))
print(next(found))

# Although it’s possible to use an assignment expression
# outside a comprehension or generator expression’s condition,
# you should avoid doing so.


# Item 30: Consider Generators Instead of Returning Lists
# The simplest choice for a function that produces a sequence of results is to return a list of items.
# A better way to write this function is by using a generator.
# Generators are produced by functions that use yield expressions.

# For example, say that I want to find the index of every word in a string.
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1


# When called, a generator function does not actually run
# but instead immediately returns an iterator.
# With each call to the next built-in function,
# the iterator advances the generator to its next yield expression.
# Each value passed to yield by the generator is returned by the iterator to the caller.
address = 'Four score and seven years ago...'
it = index_words_iter(address)
print(next(it))
print(next(it))

# You can easily convert the iterator returned by the generator to a list
# by passing it to the list built-in function if necessary.
result = list(index_words_iter(address))
print(result[:10])


# For example, here I define a generator that streams input from a file one line at a time
# and yields outputs one word at a time.
def index_file(handle):
    offset = 0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset


# The working memory for this function is limited to the maximum length of one line of input.
# Running the generator produces the same results.
import itertools

with open('address.txt', 'r') as f:
    it = index_file(f)
    results = itertools.islice(it, 0, 10)
    print(list(results))

# The only gotcha with defining generators like this is
# that the callers must be aware that the iterators returned are stateful and can’t be reused


# Item 31: Be Defensive When Iterating Over Arguments
# When a function takes a list of objects as a parameter,
# it’s often important to iterate over that list multiple times.

# For example, say that I want to analyze tourism numbers for the U.S. state of Texas.
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


# To scale this up, I need to read the data from a file that contains every city in all of Texas.
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)


# Surprisingly, calling normalize on the read_visits generator’s return value produces no results.
it = read_visits('my_numbers.txt')
percentages = normalize(it)
print(percentages)

# This behavior occurs because an iterator produces its results only a single time.
# If you iterate over an iterator or a generator that has already raised a StopIteration exception,
# you won’t get any results the second time around
visits = [15, 35, 80]
it = read_visits('my_numbers.txt')
print(list(it))  # Same with visits
print(list(it))  # [], Already exhausted

# Confusingly, you also won’t get errors when you iterate over an already exhausted iterator.
#  for loops, the list constructor, and many other functions throughout the Python standard library
#  expect the StopIteration exception to be raised during normal operation.
# These functions can’t tell the difference
# between an iterator that has no output and an iterator that had output and is now exhausted.


# To solve this problem, you can explicitly exhaust an input iterator and keep a copy of its entire contents in a list.
def normalize_copy(numbers):
    numbers_copy = list(numbers)  # Copy the iterator
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result


# Now the function works correctly on the read_visits generator’s return value
it = read_visits('my_numbers.txt')
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0


# The problem with this approach is that the copy of the input iterator’s contents could be extremely large. 
# One way around this is to accept a function that returns a new iterator each time it’s called
# To use normalize_func, I can pass in a lambda expression that calls the generator
# and produces a new iterator each time
def normalize_func(get_iter):
    total = sum(get_iter())   # New iterator
    result = []
    for value in get_iter():  # New iterator
        percent = 100 * value / total
        result.append(percent)
    return result


path = 'my_numbers.txt'
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0


# A better way to achieve the same result is to provide a new container class
# that implements the iterator protocol.
# The iterator protocol is how Python for loops and related expressions traverse the contents of a container type.
# When Python sees a statement like for x in foo, it actually calls iter(foo).
# The iter built-in function calls the foo.__iter__ special method in turn.
# The __iter__ method must return an iterator object (which itself implements the __next__ special method).
# Then, the for loop repeatedly calls the next built-in function on the iterator object
# until it’s exhausted (indi- cated by raising a StopIteration exception).
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


# This new container type works correctly when passed to the original function without modifications
visits = ReadVisits(path)
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0

# This works because the sum method in normalize calls ReadVisits.__iter__ to allocate a new iterator object.
# The for loop to normalize the numbers also calls __iter__ to allocate a second iterator object.
# Each of those iterators will be advanced and exhausted independently,
# ensuring that each unique iteration sees all the input data values.
# The only downside of this approach is that it reads the input data multiple times.


# The protocol states that when an iterator is passed to the iter built-in function, iter returns the iterator itself.
# In contrast, when a container type is passed to iter,
# a new iterator object is returned each time.
# Thus, you can test an input value for this behavior and raise a TypeError to reject arguments
# that can’t be repeatedly iterated over
def normalize_defensive(numbers):
    if iter(numbers) is numbers:  # An iterator -- bad!
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


# Alternatively, the collections.abc built-in module defines an Iterator class
# that can be used in an isinstance test to recognize the potential problem
from collections.abc import Iterator


def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):  # Another way to check
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result


# The function raises an exception if the input is an iterator rather than a container
visits = [15, 35, 80]
it = iter(visits)
normalize_defensive(it)

# Item 32: Consider Generator Expressions for Large List Comprehensions
# Use a list comprehension in a way that can only handle small input values
value = [len(x) for x in open('my_file.txt')]
print(value)  # [100, 57, 15, 1, 12, 75, 5, 86, 89, 11]

# Use generator expressions, which are a generalization of list comprehensions and generators,
# to yield one item at a time from the expression.
# Create a generator expression by putting list-comprehension-like syntax between () characters.
it = (len(x) for x in open('my_file.txt'))
print(it)
print(next(it))  # 100
print(next(it))  # 57

# Another powerful outcome of generator expressions is that they can be composed together.
# Each time I advance this iterator, it also advances the interior iterator,
# creating a domino effect of looping, evaluating conditional expressions,
# and passing around inputs and outputs, all while being as memory efficient as possible.
roots = ((x, x**0.5) for x in it)
print(next(roots))  # (15, 3.872983346207417)

# When you’re looking for a way to compose functionality that’s operating on a large stream of input,
# generator expressions are a great choice.
# The only gotcha is that the iterators returned by generator expressions are stateful,
# so you must be careful not to use these iterators more than once.

# Item 33: Compose Multiple Generators with yield from
# Generators are so useful that many programs start to look like layers of generators strung together.


# For example, say that I have a graphical program that’s using generators to animate the movement of images onscreen.
# To get the visual effect I’m looking for, I need the images to move quickly at first, pause temporarily,
# and then continue moving at a slower pace.
# Here, I define two generators that yield the expected onscreen deltas for each part of this animation:
def move(period, speed):
    for _ in range(period):
        yield speed


def pause(delay):
    for _ in range(delay):
        yield 0


# To create the final animation,
# I need to combine move and pause together to produce a single sequence of onscreen deltas.
# by calling a generator for each step of the animation, iterating over each generator in turn,
# and then yielding the deltas from all of them in sequence
def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta


# render those deltas onscreen as they’re produced by the single animation generator
def render(delta):
    print(f'Delta: {delta:.1f}')
    # Move the images onscreen
    ...


def run(func):
    for delta in func():
        render(delta)


run(animate)

# This example includes only three nested generators, and it’s already hurting clarity.


# The solution to this problem is to use the yield from expression.
# This advanced generator feature allows you to yield all values from a nested generator
# before returning control to the parent generator.
def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)


run(animate_composed)


# To verify the speedup by using the timeit built-in module to run a micro-benchmark
import timeit


def child():
    for i in range(1_000_000):
        yield i


def slow():
    for i in child():
        yield i


def fast():
    yield from child()


baseline = timeit.timeit(
    stmt='for _ in slow(): pass',
    globals=globals(),
    number=50)
print(f'Manual nesting {baseline:.2f}s')

comparison = timeit.timeit(
    stmt='for _ in fast(): pass',
    globals=globals(),
    number=50)
print(f'Composed nesting {comparison:.2f}s')

reduction = -(comparison - baseline) / baseline
print(f'{reduction:.1%} less time')

# If you find yourself composing generators,
# I strongly encourage you to use yield from when possible.

# Item 34: Avoid Injecting Data into Generators with send
# yield expressions provide generator functions with a simple way to produce an iterable series of output values.
# However, this channel appears to be unidirectional:
# There’s no immediately obvious way to simultaneously stream data
# in and out of a generator as it runs.
# Having such bidirectional communication could be valuable for a variety of use cases.

# For example, say that I’m writing a program to transmit signals using a software-defined radio.
# Here, I use a function to generate an approximation of a sine wave with a given number of points:
import math


def wave(amplitude, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output


# Transmit the wave signal at a single specified amplitude by iterating over the wave generator.
def transmit(output):
    if output is None:
        print(f'Output is None')
    else:
        print(f'Output: {output:>5.1f}')


def run(it):
    for output in it:
        transmit(output)


run(wave(3.0, 8))

# This works fine for producing basic waveforms,
# but it can’t be used to constantly vary the amplitude of the wave based on a separate input.
# I need a way to modulate the amplitude on each iteration of the generator.

# Python generators support the send method, which upgrades yield expressions into a two-way channel.
# The send method can be used to provide streaming inputs to a generator at the same time it’s yielding outputs.


# Normally, when iterating a generator, the value of the yield expression is None
def my_generator():
    received = yield 1
    print(f'received = {received}')


it = iter(my_generator())
output = next(it)  # Get first generator output
print(f'output = {output}')

try:
    next(it)  # Run generator until it exits
except StopIteration:
    pass

# When I call the send method instead of iterating the generator with a for loop or the next built-in function,
# the supplied parameter becomes the value of the yield expression when the generator is resumed.
# However, when the generator first starts, a yield expression has not been encountered yet,
# so the only valid value for calling send initially is None (any other argument would raise an exception at runtime)
it = iter(my_generator())
output = it.send(None)  # Get first generator output
print(f'output = {output}')

try:
    it.send('hello!')  # Send value into the generator
except StopIteration:
    pass


# Take advantage of this behavior in order to modulate the amplitude of the sine wave based on an input signal
def wave_modulating(steps):
    step_size = 2 * math.pi / steps
    amplitude = yield             # Receive initial amplitude
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        amplitude = yield output  # Receive next amplitude


# Update the run function to stream the modulating amplitude into the wave_modulating generator on each iteration.
def run_modulating(it):
    amplitudes = [
        None, 7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    for amplitude in amplitudes:
        output = it.send(amplitude)
        transmit(output)


run_modulating(wave_modulating(12)) # The first output is None, as expected


# Now, imagine that the program’s requirements get more complicated.
# Instead of using a simple sine wave as my carrier, I need to use a complex waveform
# consisting of multiple signals in sequence.

# One way to implement this behavior is by composing multiple generators together
# by using the yield from expression.
def complex_wave():
    yield from wave(7.0, 3)
    yield from wave(2.0, 4)
    yield from wave(10.0, 5)


run(complex_wave())


# The easiest solution is to pass an iterator into the wave function.
# The iterator should return an input amplitude each time the next built-in function is called on it.
# This arrangement ensures that each generator is progressed in a cascade as inputs and outputs are processed.
def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it)  # Get next input
        output = amplitude * fraction
        yield output


# Iterators are stateful, and thus each of the nested generators picks up where the previous generator left off
def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)


def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    it = complex_wave_cascading(iter(amplitudes))
    for amplitude in amplitudes:
        output = next(it)
        transmit(output)


run_cascading()

# Providing an input iterator to a set of composed generators is a better approach than using the send method,
# which should be avoided.
# The only downside is that this code assumes that the input generator is completely thread safe,
# which may not be the case.
# If you need to cross thread boundaries, async functions may be a better fit.

# Item 35: Avoid Causing State Transitions in Generators with throw
# Another advanced generator feature is the throw method for re-raising Exception instances within generator functions.
# The way throw works is simple:
# When the method is called, the next occurrence of a yield expression re-raises the provided Exception instance
# after its output is received instead of continuing normally.


class MyError(Exception):
    pass


def my_generator():
    yield 1
    yield 2
    yield 3


it = my_generator()
print(next(it))  # Yield 1
print(next(it))  # Yield 2
print(it.throw(MyError('test error')))


# When you call throw, the generator function may catch the injected exception
# with a standard try/except compound statement that surrounds the last yield expression
# that was executed
def my_generator():
    yield 1
    try:
        yield 2
    except MyError:
        print('Got MyError!')
    else:
        yield 3
    yield 4


it = my_generator()
print(next(it))  # Yield 1
print(next(it)) # Yield 2
# The throw method can be used to re-raise exceptions within generators
# at the position of the most recently executed yield expression.
print(it.throw(MyError('test error')))

# This functionality provides a two-way communication channel
# between a generator and its caller that can be useful in certain situations.


# For example, imagine that I’m trying to write a pro- gram with a timer that supports sporadic resets.
class Reset(Exception):
    pass


def timer(period):
    current = period
    while current:
        current -= 1
        try:
            yield current
        except Reset:
            current = period


# I can connect this counter reset event to an external input that’s polled every second.
# Then, I can define a run function to drive the timer generator, which injects exceptions with throw
# to cause resets, or calls announce for each generator output.
def check_for_reset():
    # Poll for external event
    ...


def announce(remaining):
    print(f'{remaining} ticks remaining')


def run():
    it = timer(4)
    while True:
        try:
            if check_for_reset():
                current = it.throw(Reset())
            else:
                current = next(it)
        except StopIteration:
            break
        else:
            announce(current)


run()


# A simpler approach to implementing this functionality is to define a stateful closure
# using an iterable container object
class Timer:
    def __init__(self, period):
        self.current = period
        self.period = period

    def reset(self):
        self.current = self.period

    def __iter__(self):
        while self.current:
            self.current -= 1
            yield self.current


def run():
    timer = Timer(4)
    for current in timer:
        if check_for_reset():
            timer.reset()
        announce(current)

# Often, what you’re trying to accomplish by mixing generators and exceptions is better achieved
# with asynchronous features.
# Thus, I suggest that you avoid using throw entirely and instead use an iterable class
# if you need this type of exceptional behavior.

# Item 36: Consider itertools for Working with Iterators and Generators
# The itertools built-in module contains a large number of functions
# that are useful for organizing and interacting with iterators
import itertools

# Whenever you find yourself dealing with tricky iteration code,
# it’s worth looking at the itertools documentation again
# to see if there’s anything in there for you to use
help(itertools)


# Linking Iterators Together
# The itertools built-in module includes a number of functions for linking iterators together.

# Use chain to combine multiple iterators into a single sequential iterator
it = itertools.chain([1, 2, 3], [4, 5, 6])
print(list(it))

# Use repeat to output a single value forever, or use the second parameter to specify a maximum number of times
it = itertools.repeat('hello', 3)
print(list(it))

# Use cycle to repeat an iterator’s items forever
it = itertools.cycle([1, 2])
result = [next(it) for _ in range (10)]
print(result)

# Use tee to split a single iterator into the number of parallel iterators specified by the second parameter
# The memory usage of this function will grow
# if the iterators don’t progress at the same speed since buffering will be required to enqueue the pending items
it1, it2, it3 = itertools.tee(['first', 'second'], 3)
print(list(it1))
print(list(it2))
print(list(it3))

# zip_longest returns a placeholder value when an iterator is exhausted,
# which may happen if iterators have different lengths
keys = ['one', 'two', 'three']
values = [1, 2]
normal = list(zip(keys, values))
print('zip:        ', normal)
it = itertools.zip_longest(keys, values, fillvalue='nope')
longest = list(it)
print('zip_longest:', longest)


# Filtering Items from an Iterator
# Use islice to slice an iterator by numerical indexes without copying.
# You can specify the end, start and end, or start, end, and step sizes,
# and the behavior is similar to that of standard sequence slicing and striding
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
first_five = itertools.islice(values, 5)
print('First five: ', list(first_five))
middle_odds = itertools.islice(values, 2, 8, 2)
print('Middle odds:', list(middle_odds))

# takewhile returns items from an iterator until a predicate function returns False for an item
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, values)
print(list(it))

# dropwhile
# dropwhile, which is the opposite of takewhile,
# skips items from an iterator until the predicate function returns True for the first time
less_than_seven = lambda x: x < 7
it = itertools.dropwhile(less_than_seven, values)
print(list(it))

# filterfalse, which is the opposite of the filter built-in function,
# returns all items from an iterator where a predicate function returns False
evens = lambda x: x % 2 == 0
filter_result = filter(evens, values)
print('Filter:      ', list(filter_result))

filter_false_result = itertools.filterfalse(evens, values)
print('Filter false:', list(filter_false_result))

# Producing Combinations of Items from Iterators
# accumulate folds an item from the iterator into a running value by applying a function that takes two parameters.
# It outputs the current accumulated result for each input value.
sum_reduce = itertools.accumulate(values)
print('Sum:   ', list(sum_reduce))


def sum_modulo_20(first, second):
    output = first + second
    return output % 20


modulo_reduce = itertools.accumulate(values, sum_modulo_20)
print('Modulo:', list(modulo_reduce))

# This is essentially the same as the reduce function from the functools built-in module,
# but with outputs yielded one step at a time.
# By default, it sums the inputs if no binary function is specified.

from functools import reduce

assert reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])==15

# product returns the Cartesian product of items from one or more iterators,
# which is a nice alternative to using deeply nested list comprehensions
single = itertools.product([1, 2], repeat=2)
print('Single:  ', list(single))
multiple = itertools.product([1, 2], ['a', 'b'])
print('Multiple:', list(multiple))

# permutations returns the unique ordered permutations of length N with items from an iterator
it = itertools.permutations([1, 2, 3, 4], 2)
print(list(it))

# combinations returns the unordered combinations of length N with unrepeated items from an iterator
it = itertools.combinations([1, 2, 3, 4], 2)
print(list(it))

# combinations_with_replacement is the same as combinations, but repeated values are allowed
it = itertools.combinations_with_replacement([1, 2, 3, 4], 2)
print(list(it))
