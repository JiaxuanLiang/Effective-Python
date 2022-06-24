# -*- coding: utf-8 -*- 
"""
--------------------------------------------------
File Name:        Chap2_Lists_and_Dictionaries
Description:    
Author:           jiaxuanliang
Date:             6/13/22
--------------------------------------------------
Change Activity:  6/13/22
--------------------------------------------------
"""

# Lists are extremely versatile and can be used to solve a variety of problems.
# A natural complement to lists is the dict type,
# which stores lookup keys mapped to corresponding values
# (in what is often called an associative array or a hash table).

# Item 11: Know How to Slice Sequences
# Slicing can be extended to any Python class
# that implements the __getitem__ and __setitem__ special methods
# When slicing from the start of a list,
# you should leave out the zero index to reduce visual noise
# When slicing to the end of a list, you should leave out the final index
# because it’s redundant

# Slicing deals properly with start and end indexes that are beyond the boundaries of a list
# by silently omitting missing items.
# This behavior makes it easy for your code
# to establish a maximum length to consider for an input sequence
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
first_twenty_items = a[:20]
last_twenty_items = a[-20:]
a[20]

# Modifying the result of slicing won’t affect the original list
b = a[3:]
print('Before:   ', b)
b[1] = 99
print('After:    ', b)
print('No change:', a)

# When used in assignments,
# slices replace the specified range in the original list.
# Unlike unpacking assignments,
# the lengths of slice assignments don’t need to be the same.
print('Before ', a)
a[2:7] = [99, 22, 14]
print('After  ', a)

# If you assign to a slice with no start or end indexes,
# you replace the entire contents of the list with a copy
# of what’s referenced (instead of allocating a new list)
b = a
print('Before a', a)
print('Before b', b)
a[:] = [101, 102, 103]
assert a is b  # Still the same list object
print('After a ', a)  # Now has different contents
print('After b ', b)  # Same list, so same contents as a

# Item 12: Avoid Striding and Slicing in a Single Expression
# Python has special syntax for the stride of a slice in the form somelist[start:end:stride]
x = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
odds = x[::2]
evens = x[1::2]
print(odds)
print(evens)

# To prevent problems, avoid using a stride along with start and end indexes.
# If you must use a stride, prefer making it a positive value and omit start and end indexes.
# If you must use a stride with start or end indexes, consider
# using one assignment for striding and another for slicing.
# If your program can’t afford the time or memory required for two steps,
# consider using the itertools built-in module’s islice method.

# Item 13: Prefer Catch-All Unpacking Over Slicing
# Python also supports catch-all unpacking through a starred expression.
# This syntax allows one part of the unpacking assignment to receive all values
# that didn’t match any other part of the unpacking pattern.
# A starred expression may appear in any position,
# so you can get the benefits of catch-all unpacking anytime you need to extract one slice
# You can’t use a catch-all expression on its own
car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)
oldest, second_oldest, *others = car_ages_descending
print(oldest, second_oldest, others)

# It is possible to use multiple starred expressions in an unpacking assignment statement,
# as long as they’re catch-alls for different parts of the multilevel structure being unpacked
# I don’t recommend doing the following,
# but understanding it should help you develop an intuition
# for how starred expressions can be used in unpacking assignments
car_inventory = {
    'Downtown': ('Silver Shadow', 'Pinto', 'DMC'),
    'Airport': ('Skyline', 'Viper', 'Gremlin', 'Nova'),
}
((loc1, (best1, *rest1)),
 (loc2, (best2, *rest2))) = car_inventory.items()
print(f'Best at {loc1} is {best1}, {len(rest1)} others')
print(f'Best at {loc2} is {best2}, {len(rest2)} others')

# Starred expressions become list instances in all cases.
# If there are no leftover items from the sequence being unpacked,
# the catch-all part will be an empty list.
short_list = [1, 2]
first, second, *rest = short_list
print(first, second, rest)

# You can also unpack arbitrary iterators with the unpacking syntax.
it = iter(range(1, 3))
first, second = it
print(f'{first} and {second}')


# With the addition of starred expressions,
# the value of unpacking iterators becomes clear
def generate_csv():
    yield 'Date', 'Make', 'Model', 'Year', 'Price'
    ...


# Processing the results of this generator using indexes and slices is fine,
# but it requires multiple lines and is visually noisy
all_csv_rows = list(generate_csv())
header = all_csv_rows[0]
rows = all_csv_rows[1:]
print('CSV Header:', header)
print('Row count: ', len(rows))

# Unpacking with a starred expression makes it easy to process
# the first row—the header—separately from the rest of the iterator’s contents.
it = generate_csv()
header, *rows = it
print('CSV Header:', header)
print('Row count: ', len(rows))

# You should only use catch-all unpacking on iterators
# when you have good reason to believe that the result data will all fit in memory

# Item 14: Sort by Complex Criteria Using the key Parameter
# The list built-in type provides a sort method for ordering the items in a list instance
# based on a variety of criteria.
# By default, sort will order a list’s contents
# by the natural ascending order of the items.
numbers = [93, 86, 11, 68, 70]
numbers.sort()
print(numbers)


# The sort method works for nearly all built-in types (strings, floats, etc.) that have a natural ordering to them.
# But it does not work for objects unless they define a natural ordering using special methods, which is uncommon.
# It also accepts a key parameter that’s expected to be a function.
# The key function is passed a single argument, which is an item from the list that is being sorted.
# The return value of the key function should be a comparable value (i.e., with a natural ordering)
# to use in place of an item for sorting purposes.
class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'


tools = [
    Tool('level', 3.5),
    Tool('hammer', 1.25),
    Tool('screwdriver', 0.5),
    Tool('chisel', 0.25),
]

print('Unsorted:', repr(tools))
tools.sort(key=lambda x: x.name)
print('\nSorted:  ', tools)
tools.sort(key=lambda x: x.weight)
print('By weight:', tools)

# For basic types like strings,
# you may even want to use the key function to do transformations on the values before sorting.
places = ['home', 'work', 'New York', 'Paris']
places.sort()
print('Case sensitive:  ', places)
places.sort(key=lambda x: x.lower())
print('Case insensitive:', places)

# Sometimes you may need to use multiple criteria for sorting.
# The simplest solution in Python is to use the tuple type.
# Tuples implement these special method comparators
# by iterating over each position in the tuple and comparing the corresponding values one index at a time.
# If the first position in the tuples being compared are equal—weight
# then the tuple comparison will move on to the second position, and so on.
power_tools = [
    Tool('drill', 4),
    Tool('circular saw', 5),
    Tool('jackhammer', 40),
    Tool('sander', 4),
]
power_tools.sort(key=lambda x: (x.weight, x.name))
print(power_tools)

# One limitation of having the key function return a tuple is
# that the direction of sorting for all criteria must be the same
# For numerical values it’s possible to mix sorting directions
# by using the unary minus operator in the key function.
power_tools.sort(key=lambda x: (-x.weight, x.name))
print(power_tools)

# Python provides a stable sorting algorithm.
# The sort method of the list type will preserve the order of the input list
# when the key function returns values that are equal to each other.
# You just need to make sure that you execute the sorts in the opposite sequence
# of what you want the final list to contain.
power_tools.sort(key=lambda x: x.name)  # Name ascending
power_tools.sort(key=lambda x: x.weight, reverse=True)  # Weight descending
print(power_tools)

# Item 15: Be Cautious When Relying on dict Insertion Ordering
# In Python 3.5 and before, iterating over a dict would return keys in arbitrary order.
# This happened because the dictionary type previously implemented its hash table algorithm
# with a combination of the hash built-in function
# and a random seed that was assigned when the Python interpreter started.
# Together, these behaviors caused dictionary orderings to not match insertion order
# and to randomly shuffle between program executions.
# With Python 3.5 and earlier, all methods provided by dict that relied on iteration order,
# including keys, values, items, and popitem, would similarly demonstrate this random-looking behavior
# These methods now provide consistent insertion ordering
# that you can rely on when you write your programs
baby_names = {
    'cat': 'kitten',
    'dog': 'puppy',
}

print(baby_names)
print(list(baby_names.keys()))
print(list(baby_names.values()))
print(list(baby_names.items()))
print(baby_names.popitem())  # Last item inserted


# Now, the order of keyword arguments is always preserved
# to match how the programmer originally called the function
def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')


my_func(goose='gosling', kangaroo='joey')


# You can now assume that the order of assignment for these
# instance fields will be reflected in __dict__
class MyClass:
    def __init__(self):
        self.alligator = 'hatchling'
        self.elephant = 'calf'


a = MyClass()
for key, value in a.__dict__.items():
    print(f'{key} = {value}')

# If you need to handle a high rate of key insertions
# and popitem calls (e.g., to implement a least-recently-used cache),
# OrderedDict may be a better fit than the standard Python dict type.
# However, you shouldn’t always assume that insertion ordering behavior will be present
# when you’re handling dictionaries.
# Example: writing a program to show the results of a contest for the cutest baby animal
votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863, }


# I define a function to process this voting data
# and save the rank of each animal name into a provided empty dictionary.
# In this case, the dictionary could be the data model that powers a UI element
def populate_ranks(votes, ranks):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i


def get_winner(ranks):
    return next(iter(ranks))


ranks = {}
populate_ranks(votes, ranks)
print(ranks)
winner = get_winner(ranks)
print(winner)

#  The UI element that shows the results should be in alphabetical order instead of rank order.
from collections.abc import MutableMapping


class SortedDict(MutableMapping):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self):
        return len(self.data)


# This code is using SortedDict instead of dict,
# so that assumption is no longer true.
# Thus, the value returned for the winner is 'fox',
# which is alphabetically first.
sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner)

# when using type annotations to enforce that the value passed to get_winner is a dict instance
# and not a MutableMapping with dictionary-like behavior
# This correctly detects the mismatch between the dict and MutableMapping types
# and flags the incorrect usage as an error.
# This solution provides the best mix of static type safety and runtime performance.
from typing import Dict, MutableMapping


def populate_ranks(votes: Dict[str, int],
                   ranks: Dict[str, int]) -> None:
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i


def get_winner(ranks: Dict[str, int]) -> str:
    return next(iter(ranks))


class SortedDict(MutableMapping[str, int]):
    ...


votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863, }
sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner)

# Item 16: Prefer get Over in and KeyError to Handle Missing Dictionary Keys
# The three fundamental operations for interacting with dictionaries
# are accessing, assigning, and deleting keys and their associated values.
# There are four common ways to detect and handle missing keys in dictionaries:
# using in expressions, KeyError exceptions, the get method, and the setdefault method.

# Example: to see if the key exists, insert the key
# with a default counter value of zero if it’s missing,
# and then increment the counter’s value.
counters = {
    'pumpernickel': 2,
    'sourdough': 1,
}

# using an if statement with an in expression
key = 'wheat'
if key in counters:
    count = counters[key]
else:
    count = 0
counters[key] = count + 1

# by relying on how dictionaries raise a KeyError exception
# when you try to get the value for a key that doesn’t exist
try:
    count = counters[key]
except KeyError:
    count = 0
counters[key] = count + 1

# by the get method of the built-in type
# The second parameter to get is the default value to return
# in the case that the key—the first parameter—isn’t present.
count = counters.get(key, 0)
counters[key] = count + 1

# Example: if the values of the dictionary are a more complex type, like a list
votes = {
    'baguette': ['Bob', 'Alice'],
    'ciabatta': ['Coco', 'Deb'],
}
key = 'brioche'
who = 'Elmer'

# using get to fetch list values and an assignment expression in the if statement
# setdefault tries to fetch the value of a key in the dictionary.
if (names := votes.get(key)) is None:
    votes[key] = names = []
names.append(who)

# The dict type also provides the setdefault method.
# If the key isn’t present, the method assigns that key to the default value provided.
# And then the method returns the value for that key:
# either the originally present value or the newly inserted default value.
names = votes.setdefault(key, [])
names.append(who)

# setdefault isn’t self-explanatory
# The default value passed to setdefault is assigned directly into the dictionary
# when the key is missing instead of being copied.
# This means that I need to make sure that I’m always constructing a new default value
# for each key I access with setdefault.
data = {}
key = 'foo'
value = []
data.setdefault(key, value)
print('Before:', data)
value.append('hello')
print('After: ', data)

# Using get for updates requires only one access and one assignment,
# whereas using setdefault requires one access and two assignments.

# Item 17: Prefer defaultdict Over setdefault to Handle Missing Items in Internal State
# When working with a dictionary that you didn’t create,
# there are a variety of ways to handle missing keys
# Example: to keep track of the cities I’ve visited in countries around the world
# use the setdefault method to add new cities to the sets
visits = {
    'Mexico': {'Tulum', 'Puerto Vallarta'},
    'Japan': {'Hakone'},
}
visits.setdefault('France', set()).add('Arles')  # Short

# use the get method and an assignment expression
if (japan := visits.get('Japan')) is None:  # Long
    visits['Japan'] = japan = set()
japan.add('Kyoto')
print(visits)


# When you do control creation of the dictionary being accessed
# This is generally the case when you’re using a dictionary instance
# to keep track of the internal state of a class, for example.
# By wrapping the example above in a class with helper methods
# to access the dynamic inner state stored in a dictionary
# This new class hides the complexity of calling setdefault correctly,
# and it provides a nicer interface for the programmer
# But the implementation isn’t efficient
# because it constructs a new set instance on every call,
# regardless of whether the given country was already present in the data dictionary
class Visits:
    def __init__(self):
        self.data = {}

    def add(self, country, city):
        city_set = self.data.setdefault(country, set())
        city_set.add(city)


visits = Visits()
visits.add('Russia', 'Yekaterinburg')
visits.add('Tanzania', 'Zanzibar')
print(visits.data)


# The defaultdict class from the collections built-in module simplifies this common use case
# by automatically storing a default value when a key does not exist.
# All you have to do is provide a function
# that will return the default value to use each time a key is missing
class Visits:
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)


visits = Visits()
visits.add('England', 'Bath')
visits.add('England', 'London')
print(visits.data)

# If you’re creating a dictionary to manage an arbitrary set of potential keys,
# then you should prefer using a defaultdict instance
# from the collections built-in module if it suits your problem.

# If a dictionary of arbitrary keys is passed to you,
# and you don’t control its creation,
# then you should prefer the get method to access its items.
# However, it’s worth considering using the setdefault method
# for the few situations in which it leads to shorter code.

# Item 18: Know How to Construct Key-Dependent Default Values with __missing__
# There are times when neither setdefault nor defaultdict is the right fit.
# Example: writing a program to manage social network profile pictures on the filesystem
# I need a dictionary to map profile picture pathnames to open file handles
# so I can read and write those images as needed.

# When the file handle already exists in the dictionary,
# this code makes only a single dictionary access.
# In the case that the file handle does not exist,
# the dictionary is accessed once by get,
# and then it is assigned in the else clause of the try/except block.
pictures = {}
path = 'profile_1234.png'
if (handle := pictures.get(path)) is None:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'Failed to open path {path}')
        raise
    else:
        pictures[path] = handle
handle.seek(0)
image_data = handle.read()

# Although it’s possible to use the in expression or KeyError approaches
# to implement this same logic,
# those options require more dictionary accesses and levels of nesting.

# Given that these other options work,
# you might also assume that the setdefault method would work, too
# The open built-in function to create the file handle is always called,
# even when the path is already present in the dictionary.
# This results in an additional file handle
# that may conflict with existing open handles in the same program.
# Exceptions may be raised by the open call and need to be handled,
# but it may not be possible to differentiate them from exceptions
# that may be raised by the setdefault call on the same line
try:
    handle = pictures.setdefault(path, open(path, 'a+b'))
except OSError:
    print(f'Failed to open path {path}')
    raise
else:
    handle.seek(0)
    image_data = handle.read()

# If you’re trying to manage internal state,
# another assumption you might make is that a defaultdict could be used
# for keeping track of these profile pictures.
from collections import defaultdict


def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except OSError:
        print(f'Failed to open path {profile_path}')
        raise


# Error
# The problem is that the function passed to defaultdict must not require any arguments,
# which makes it impossible to have the default value depend on the key being accessed.
# This means that the helper function that defaultdict calls doesn’t know which specific key
# is being accessed, which eliminates my ability to call open.
pictures = defaultdict(open_picture)
handle = pictures[path]
handle.seek(0)
image_data = handle.read()


# Python has another built-in solution.
# You can define your own dict subclass with a __missing__ method
# in order to construct default values that must know which key was being accessed.
# When the pictures[path] dictionary access finds that the path key isn’t present in the dictionary,
# the __missing__ method is called.
# This method must create the new default value for the key,
# insert it into the dictionary, and return it to the caller.
# Subsequent accesses of the same path will not call __missing__
# since the corresponding item is already present
class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value


pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()
