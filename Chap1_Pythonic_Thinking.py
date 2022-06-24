# -*- coding: utf-8 -*-
"""
--------------------------------------------------
File Name:        Chap1_Pythonic_Thinking
Description:
Author:           jiaxuanliang
Date:             6/13/22
--------------------------------------------------
Change Activity:  6/13/22
--------------------------------------------------
"""

# Item 1: Know Which Version of Python You’re Using
#  To find out exactly which version of Python you’re using,
#  you can use the --version flag:
# (in terminal) $ python --version
# (in terminal) $ python3 --version

# You can also figure out the version of Python you’re using at runtime
# by inspecting values in the sys built-in module:
import sys
print(sys.version_info)
print(sys.version)

# Item 2: Follow the PEP 8 Style Guide
# Python Enhancement Proposal #8, otherwise known as PEP 8,
# is the style guide for how to format Python code.
# https://www.python.org/dev/peps/pep-0008/

# Item 3: Know the Differences Between bytes and str
# In Python, there are two types that represent sequences of character data:
# bytes and str.

# Instances of bytes contain raw, unsigned 8-bit values
# (often displayed in the ASCII encoding)
a = b'h\x65llo'
print(list(a))
print(a)

# Instances of str contain Unicode code points
# that represent textual characters from human languages
a = 'a\u0300 propos'
print(list(a))
print(a)

# Importantly, str instances do not have an associated binary encoding,
# and bytes instances do not have an associated text encoding.
# Byte contains sequences of 8-bit values, and str contains sequences of Unicode code points.
# Bytes and str instances can’t be used together with operators (like >, ==, +, and %).
# The core of your program should use the str type containing Unicode data
# and should not assume anything about character encodings.


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str


print(repr(to_str(b'foo')))
print(repr(to_str('bar')))


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of bytes


print(repr(to_bytes(b'foo')))
print(repr(to_bytes('bar')))

#  When a file is in text mode,
#  write operations expect str instances containing Unicode data
#  instead of bytes instances containing binary data.
with open('data.bin', 'w') as f:
    f.write(b'\xf1\xf2\xf3\xf4\xf5')

with open('data.bin', 'wb') as f:
    f.write(b'\xf1\xf2\xf3\xf4\xf5')

# When a handle is in text mode,
# it uses the system’s default text encoding to interpret binary data
# using the bytes.encode (for writing) and str.decode (for reading) methods. On most systems,
# the default encoding is UTF-8, which can’t accept the binary data b'\xf1\xf2\xf3\xf4\xf5',
# thus causing the error above.
with open('data.bin', 'r') as f:
    data = f.read()

with open('data.bin', 'rb') as f:
    data = f.read()

assert data == b'\xf1\xf2\xf3\xf4\xf5'

# Alternatively, I can explicitly specify the encoding parameter to the open function
# to make sure that I’m not surprised by any platform-specific behavior.
with open('data.bin', 'r', encoding='cp1252') as f:
    data = f.read()

assert data == 'ñòóôõ'

# The lesson here is that you should check the default encoding on your system
# (in terminal)python3 - c 'import locale; print(locale. getpreferredencoding())')

# Item 4: Prefer Interpolated F-Strings Over C-style Format Strings and str.format
# Formatting is the process of combining predefined text with data values into a single human-readable message
# that’s stored as a string.

# The most common way to format a string in Python is by using the old C-style format strings
# that use the % formatting operator.
# The predefined text template is provided on the left side of the operator in a format string.
# The values to insert into the template are provided as a single value or tuple of multiple values
# on the right side of the format operator.
a = 0b10111011
b = 0xc5f
print('Binary is %d, hex is %d' % (a, b))

# The % operator in Python has the ability to also do formatting with a dictionary instead of a tuple
key = 'my_var'
value = 1.234
old_way = '%-10s = %.2f' % (key, value)
new_way = '%(key)-10s = %(value).2f' % {'key': key, 'value': value}  # Original
reordered = '%(key)-10s = %(value).2f' % {'value': value, 'key': key}  # Swapped
assert old_way == new_way == reordered

# With C-style format strings, you need to escape the % character (by doubling it)
# so it’s not interpreted as a placeholder accidentally.
print('%.2f%%' % 12.5)

# The format Built-in and str.format
a = 1234.5678
formatted = format(a, ',.2f')  # , for thousands separators
print(formatted)

b = 'my string'
formatted = format(b, '^20s')  # ^ for centering
print('*', formatted, '*')

# Instead of using C-style format specifiers like %d,
# you can specify placeholders with {}.
key = 'my_var'
value = 1.234
formatted = '{} = {}'.format(key, value)
print(formatted)

# Within each placeholder you can optionally provide a colon character
# followed by format specifiers to customize how values will be converted into strings
# (see help('FORMATTING') for the full range of options)

# The way to think about how this works is that the format specifiers will be passed
# to the format built-in function along with the value (format(value, '.2f') in the example above).
# The result of that function call is what replaces the placeholder in the overall formatted string.
# The formatting behavior can be customized per class using the __format__ special method.
formatted = '{:<10} = {:.2f}'.format(key, value)
print(formatted)

# With the str.format method you need to escape braces
print('{} replaces {{}}'.format(1.23))

# Within the braces you may also specify the positional index of an argument passed to the format method
# to use for replacing the placeholder.
# This allows the format string to be updated to reorder the output
# without requiring you to also change the right side of the formatting expression.
formatted = '{1} = {0}'.format(key, value)
print(formatted)

# The same positional index may also be referenced multiple times in the format string without the need
# to pass the value to the format method more than once.
name = 'Max'
formatted = '{0} loves food. See {0} cook.'.format(name)
print(formatted)

# There are even more advanced options for the specifiers used with the str.format method,
# such as using combinations of dictionary keys and list indexes in placeholders,
# and coercing values to Unicode and repr strings
menu = {
    'soup': 'lentil',
    'oyster': 'kumamoto',
    'special': 'schnitzel',
}
formatted = 'First letter is {menu[oyster][0]!r}'.format(
    menu=menu)
print(formatted)

old_template = (
    'Today\'s soup is %(soup)s, '
    'buy one get two %(oyster)s oysters, '
    'and our special entrée is %(special)s.')
old_formatted = old_template % {
    'soup': 'lentil',
    'oyster': 'kumamoto',
    'special': 'schnitzel',
}
new_template = (
    'Today\'s soup is {soup}, '
    'buy one get two {oyster} oysters, '
    'and our special entrée is {special}.')
new_formatted = new_template.format(
    soup='lentil',
    oyster='kumamoto',
    special='schnitzel',
)
assert old_formatted == new_formatted

# Interpolated Format Strings
# Python 3.6 added interpolated format strings—f-strings for short
# This new language syntax requires you to prefix format strings with an f character,
# which is similar to how byte strings are prefixed with a b character
# and raw (unescaped) strings are prefixed with an r character.
key = 'my_var'
value = 1.234
formatted = f'{key} = {value}'
print(formatted)

# They achieve this pithiness by allowing you to reference all names in the current Python scope
# as part of a formatting expression
# All of the same options from the new format built-in mini language are available
# after the colon in the placeholders within an f-string,
# as is the ability to coerce values to Unicode and repr strings similar to the str.format method.
formatted = f'{key!r:<10} = {value:.2f}'
print(formatted)

# Formatting with f-strings is shorter than using C-style format strings with the % operator
# and the str.format method in all cases.
f_string = f'{key:<10} = {value:.2f}'
c_tuple  = '%-10s = %.2f' % (key, value)
str_args = '{:<10} = {:.2f}'.format(key, value)
str_kw   = '{key:<10} = {value:.2f}'.format(key=key, value=value)
c_dict   = '%(key)-10s = %(value).2f' % {'key': key, 'value': value}
assert c_tuple == c_dict == f_string
assert str_args == str_kw == f_string

# F-strings also enable you to put a full Python expression
# within the placeholder braces
pantry = [
    ('avocados', 1.25),
    ('bananas', 2.5),
    ('cherries', 15),
]
for i, (item, count) in enumerate(pantry):
    old_style = '#%d: %-10s = %d' % (
        i + 1,
        item.title(),
        round(count))
    new_style = '#{}: {:<10s} = {}'.format(
        i + 1,
        item.title(),
        round(count))
    f_string = f'#{i+1}: {item.title():<10s} = {round(count)}'
    assert old_style == new_style == f_string

# Python expressions may also appear within the format specifier options.
places = 3
number = 1.23456
print(f'My number is {number:.{places}f}')

# The combination of expressiveness, terseness, and clarity provided by f-strings makes them the best built-in option
# for Python programmers. Any time you find yourself needing to format values into strings,
# choose f-strings over the alternatives.

# Item 5: Write Helper Functions Instead of Complex Expressions
# Python’s pithy syntax makes it easy to write single-line expressions that implement a lot of logic.
# For example, say that I want to decode the query string from a URL.
# Here, each query string parameter represents an integer value:
from urllib.parse import parse_qs
my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
print(repr(my_values))
print('Red:     ', my_values.get('red'))
print('Green:   ', my_values.get('green'))
print('Opacity: ', my_values.get('opacity'))

# It’d be nice if a default value of 0 were assigned when a parameter isn’t supplied or is blank.
# Python’s syntax makes this choice all too easy.
# The trick here is that the empty string, the empty list, and zero all evaluate to False implicitly.
# For query string 'red=5&blue=0&green='
# The behavior of the get method is to return its second argument
# if the key does not exist in the dictionary.
red = my_values.get('red', [''])[0] or 0
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0
print(f'Red:     {red!r}')
print(f'Green:   {green!r}')
print(f'Opacity: {opacity!r}')

# I’d also want to ensure that all the parameter val- ues are converted to integers
# so I can immediately use them in mathematical expressions.

# Extremely hard to read.
# Even though it’s nice to keep things short,
# it’s not worth trying to fit this all on one line.
red = int(my_values.get('red', [''])[0] or 0)

# Python has if/else conditional—or ternary—expressions
# to make cases like this clearer while keeping the code short
# Not as clear as the alternative of a full if/else statement over multiple lines.
red_str = my_values.get('red', [''])
red = int(red_str[0]) if red_str[0] else 0

# Seeing all the logic spread out like this makes the dense version seem even more complex
green_str = my_values.get('green', [''])
if green_str[0]:
    green = int(green_str[0])
else:
    green = 0


# If you need to reuse this logic repeatedly—even just two or three times,
# as in this example—then writing a helper function is the way to go
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default


green = get_first_int(my_values, 'green')

# What you gain in readability always outweighs what brevity may have afforded you.
# Follow the DRY principle: Don’t repeat yourself.

# Item 6: Prefer Multiple Assignment Unpacking Over Indexing
# Python has a built-in tuple type that can be used to create immutable, ordered sequences of values.
snack_calories = {
    'chips': 140,
    'popcorn': 80,
    'nuts': 190,
}
items = tuple(snack_calories.items())
print(items)

# The values in tuples can be accessed through numerical indexes
item = ('Peanut butter', 'Jelly')
first = item[0]
second = item[1]
print(first, 'and', second)

# Once a tuple is created,
# you can’t modify it by assigning a new value to an index
pair = ('Chocolate', 'Peanut butter')
pair[0] = 'Honey'

# Python also has syntax for unpacking,
# which allows for assigning multiple values in a single statement.
item = ('Peanut butter', 'Jelly')
first, second = item  # Unpacking
print(first, 'and', second)

# Unpacking has less visual noise than accessing the tuple’s indexes,
# and it often requires fewer lines.
# The same pattern matching syntax of unpacking works
# when assigning to lists, sequences, and multiple levels of arbitrary iterables within iterables.
# I don’t recommend doing the following in your code,
# but it’s important to know that it’s possible and how it works
favorite_snacks = {
    'salty': ('pretzels', 100),
    'sweet': ('cookies', 180),
    'veggie': ('carrots', 20),
}
((type1, (name1, cals1)),
 (type2, (name2, cals2)),
 (type3, (name3, cals3))) = favorite_snacks.items()
print(f'Favorite {type1} is {name1} with {cals1} calories')
print(f'Favorite {type2} is {name2} with {cals2} calories')
print(f'Favorite {type3} is {name3} with {cals3} calories')


# Unpacking can even be used to swap values in place
# without the need to create temporary variables
# Example using typical syntax
def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i-1]:
                temp = a[i]
                a[i] = a[i-1]
                a[i-1] = temp


names = ['pretzels', 'carrots', 'arugula', 'bacon']
bubble_sort(names)
print(names)


# Example using unpacking syntax
def bubble_sort(a):
    for _ in range(len(a)):
        for i in range(1, len(a)):
            if a[i] < a[i-1]:
                a[i-1], a[i] = a[i], a[i-1]  # Swap


names = ['pretzels', 'carrots', 'arugula', 'bacon']
bubble_sort(names)
print(names)

# Another valuable application of unpacking
# is in the target list of for loops and similar constructs,
# such as comprehensions and generator expressions
snacks = [('bacon', 350), ('donut', 240), ('muffin', 190)]
for rank, (name, calories) in enumerate(snacks, 1):
    print(f'#{rank}: {name} has {calories} calories')

# Item 7: Prefer enumerate Over range
# The range built-in function is useful for loops that iterate over a set of integers
from random import randint
random_bits = 0
for i in range(32):
    if randint(0, 1):
        random_bits |= 1 << i  # 1 << i has higher priority
print(bin(random_bits))

# enumerate wraps any iterator with a lazy generator
# The second parameter specifies the number
# from which to begin counting (zero is the default).
flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
it = enumerate(flavor_list)
print(next(it))
print(next(it))

# Item 8: Use zip to Process Iterators in Parallel
# List comprehensions make it easy to take a source list and get a derived list by applying an expression.
names = ['Cecilia', 'Lise', 'Marie']
counts = [len(n) for n in names]
print(counts)

# The items in the derived list are related to the items in the source list by their indexes.
# Python provides the zip built-in function.
# zip wraps two or more iterators with a lazy generator.
# The zip generator yields tuples containing the next value from each iterator.
for name, count in zip(names, counts):
    if count > max_count:
        longest_name = name
        max_count = count

# zip consumes the iterators it wraps one item at a time, which means it can be used with infinitely long inputs
# without risk of a program using too much memory and crashing.
# It keeps yielding tuples until any one of the wrapped iter- ators is exhausted.
# Its output is as long as its shortest input.
# If you don’t expect the lengths of the lists passed to zip to be equal,
# consider using the zip_longest function from the itertools built-in module instead
# zip_longest replaces missing values—the length of the string 'Rosalind' in this case
# -with whatever fillvalue is passed to it, which defaults to None.
import itertools
names.append('Rosalind')
for name, count in itertools.zip_longest(names, counts):
    print(f'{name}: {count}')

# Item 9: Avoid else Blocks After for and while Loops
# You can put an else block immediately after a loop’s repeated interior block
for i in range(3):
    print('Loop', i)
else:
    print('Else block!')

# Using a break statement in a loop actually skips the else block
for i in range(3):
    print('Loop', i)
    if i == 1:
        break
else:
    print('Else block!')

# Another surprise is that the else block runs immediately if you loop over an empty sequence
for x in []:
    print('Never runs')
else:
    print('For Else block!')

# The else block also runs when while loops are initially False
while False:
    print('Never runs')
else:
    print('While Else block!')

# The rationale for these behaviors is that else blocks after loops are useful
# when using loops to search for something.
a=4
b=9
for i in range(2, min(a, b) + 1):
    print('Testing', i)
    if a % i == 0 and b % i == 0:
        print('Not coprime')
        break
else:
    print('Coprime')


# In practice, I wouldn’t write the code this way. Instead,
# I’d write a helper function to do the calculation.
# Such a helper function is writ- ten in two common styles.
def coprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True


assert coprime(4, 9)
assert not coprime(3, 6)


# The second way is to have a result variable
# that indicates whether I’ve found what I’m looking for in the loop.
# I break out of the loop as soon as I find something.
def coprime_alternate(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime


assert coprime_alternate(4, 9)
assert not coprime_alternate(3, 6)


# However, the expressivity you gain from the else block doesn’t outweigh the burden you put on people
# (including yourself) who want to understand your code in the future.
# Avoid using else blocks after loops because their behavior isn’t intuitive and can be confusing.

# Item 10: Prevent Repetition with Assignment Expressions
# An assignment expression—also known as the walrus operator
# —is a new syntax introduced in Python 3.8 to solve a long-standing problem with the language
# that can cause code duplication.

# Whereas normal assignment statements are written a = b and pronounced “a equals b,”
# these assignments are written a := b and pronounced “a walrus b”
# (because := looks like a pair of eyeballs and tusks).
# An assignment expression’s value evaluates to whatever was assigned to the identifier
# on the left side of the walrus operator.

# This pattern of fetching a value, checking to see if it’s non-zero,
# and then using it is extremely common in Python.
# Assignment expressions were added to the language to streamline exactly this type of code.
# This two-step behavior—assign and then evaluate—is the fundamental nature of the walrus operator.
def make_lemonade(count):
    ...


def make_cider(count):
    ...


def out_of_stock():
    ...


if count := fresh_fruit.get('lemon', 0):
    make_lemonade(count)
else:
    out_of_stock()

# When an assignment expression is a subexpression of a larger expression,
# it must be surrounded with parentheses.
# (You should avoid surrounding assignment expressions with parentheses when possible)
if (count := fresh_fruit.get('apple', 0)) >= 4:
    make_cider(count)
else:
    out_of_stock()


# Another common variation of this repetitive pattern occurs
# when I need to assign a variable in the enclosing scope depending on some condition, and then reference
# that variable shortly afterward in a function call.
def slice_bananas(count):
    ...


class OutOfBananas(Exception):
    pass


def make_smoothies(count):
    ...

if (count := fresh_fruit.get('banana', 0)) >= 2:
    pieces = slice_bananas(count)
else:
    pieces = 0
try:
    smoothies = make_smoothies(pieces)
except OutOfBananas:
    out_of_stock()


# One frustration that programmers who are new to Python often have is the lack of a flexible switch/case statement.
# The general style for approximating this type of functionality is to have a deep nesting
# of multiple if, elif, and else statements.
if (count := fresh_fruit.get('banana', 0)) >= 2:
    pieces = slice_bananas(count)
    to_enjoy = make_smoothies(pieces)
elif (count := fresh_fruit.get('apple', 0)) >= 4:
    to_enjoy = make_cider(count)
elif count := fresh_fruit.get('lemon', 0):
    to_enjoy = make_lemonade(count)
else:
    to_enjoy = 'Nothing'


# Another common frustration of new Python programmers is the lack of a do/while loop construct.
def pick_fruit():
    ...


def make_juice(fruit, count):
    ...


bottles = []
fresh_fruit = pick_fruit()
while fresh_fruit:
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)
    fresh_fruit = pick_fruit()

# A strategy for improving code reuse in this situation is
# to use the loop-and-a-half idiom.
# This eliminates the redundant lines,
# but it also undermines the while loop’s contribution by making it a dumb infinite loop.
bottles = []
while True:  # Loop
    fresh_fruit = pick_fruit()
    if not fresh_fruit:  # And a half
        break
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

# The walrus operator obviates the need for the loop-and-a-half idiom
# by allowing the fresh_fruit variable to be reassigned and then conditionally evaluated
# each time through the while loop.
bottles = []
while fresh_fruit := pick_fruit():
    for fruit, count in fresh_fruit.items():
        batch = make_juice(fruit, count)
        bottles.extend(batch)

# In general, when you find yourself repeating the same expression or assignment multiple times
# within a grouping of lines, it’s time to consider using assignment expressions
# in order to improve readability.
