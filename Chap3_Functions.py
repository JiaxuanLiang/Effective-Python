# -*- coding: utf-8 -*- 
"""
--------------------------------------------------
File Name:        Chap3_Functions
Description:    
Author:           jiaxuanliang
Date:             6/14/22
--------------------------------------------------
Change Activity:  6/14/22
--------------------------------------------------
"""


# Item 19: Never Unpack More Than Three Variables When Functions Return Multiple Values
# To avoid these problems, you should never use more than three variables
# when unpacking the multiple return values from a function.
# These could be individual values from a three-tuple,
# two variables and one catch-all starred expression, or anything shorter.
# If you need to unpack more return values than that, you’re better off
# defining a lightweight class or namedtuple
# and having your function return an instance of that instead.

# Item 20: Prefer Raising Exceptions to Returning None
# When writing utility functions, there’s a draw for Python programmers
# to give special meaning to the return value of None.
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


x, y = 1, 0
result = careful_divide(x, y)
if result is None:
    print('Invalid inputs')


# To reduce the chance of errors
def careful_divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None


success, result = careful_divide(x, y)
if not success:
    print('Invalid inputs')


# Better way to reduce these errors is to never return None for special cases
# Instead, raise an Exception up to the caller and have the caller deal with it.
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs')


x, y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)

# Type annotations can be used to make it clear that a function will never return the value None,
# even in special situations.
# what this function should look like when using type annotations and docstrings
    def careful_divide(a: float, b: float) -> float:
        """Divides a by b.
        Raises:
            ValueError: When the inputs cannot be divided.
    """
        try:
            return a / b
        except ZeroDivisionError as e:
            raise ValueError('Invalid inputs')


# Item 21: Know How Closures Interact with Variable Scope
# Say that I want to sort a list of numbers but prioritize one group of numbers to come first.
# A common way to do this is to pass a helper function as the key argument to a list’s sort method
# Closure functions can refer to variables from any of the scopes in which they were defined.
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)


numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)


# Use the closure to flip a flag when high-priority items are seen
# But the found result returned by the function is False when it should be True.
# This problem is sometimes called the scoping bug.
# By default, closures can’t affect enclosing scopes by assigning variables.
# This prevents local variables in a function from polluting the containing module.
def sort_priority2(numbers, group):
    found = False  # Scope: 'sort_priority2'

    def helper(x):
        if x in group:
            found = True  # Seems simple, but Scope: 'helper' -- Bad!
            return (0, x)
        return (1, x)

    numbers.sort(key=helper)
    return found


found = sort_priority2(numbers, group)
print('Found:', found)
print(numbers)


# Use the nonlocal statement to indicate
# when a closure can modify a variable in its enclosing scopes.
# It’s complementary to the global statement,
# which indicates that a variable’s assignment should go
# directly into the module scope.
def sort_priority3(numbers, group):
    found = False

    def helper(x):
        nonlocal found  # Added
        if x in group:
            found = True
            return (0, x)
        return (1, x)

    numbers.sort(key=helper)
    return found


# However, much as with the anti-pattern of global variables,
# I’d caution against using nonlocal for anything beyond simple functions.
# When your usage of nonlocal starts getting complicated,
# it’s better to wrap your state in a helper class.
class Sorter:
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)


sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True


# Item 22: Reduce Visual Noise with Variable Positional Arguments
# Accepting a variable number of positional arguments
# can make a function call clearer and reduce visual noise.
# (These positional arguments are often called varargs for short,
# or star args, in reference to the conventional name for the parameter *args.)
def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')


log('My numbers are', [1, 2])
log('Hi there', [])


# Having to pass an empty list when I have no values to log is cumbersome and noisy.
# It’d be better to leave out the second argument entirely.
def log(message, *values):  # The only difference
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')


log('My numbers are', [1, 2])
log('Hi there')  # Much better

# Variadic: In computer science, an operator or function is variadic
# if it can take a varying number of arguments;
# that is, if its arity is not fixed.
# If I already have a sequence (like a list)
# and want to call a variadic function like log,
# I can do this by using the * operator.
# This instructs Python to pass items from the sequence
# as positional arguments to the function.
favorites = [7, 33, 99]
log('Favorite colors', *favorites)


# These optional positional arguments are always turned into a tuple
# before they are passed to a function.
# This means that if the caller of a function uses the * operator
# on a generator, it will be iterated until it’s exhausted
# The resulting tuple includes every value from the generator,
# which could consume a lot of memory and cause the program to crash
def my_generator():
    for i in range(10):
        yield i


def my_func(*args):
    print(args)


it = my_generator()
my_func(*it)


# Functions that accept *args are best for situations where you know
# the number of inputs in the argument list will be reasonably small.
# *args is ideal for function calls that pass many literals or variable names together.
# It’s primarily for the convenience of the programmer and the readability of the code.

# You can’t add new positional arguments to a function in the future
# without migrating every caller.
def log(sequence, message, *values):
    if not values:
        print(f'{sequence} - {message}')
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{sequence} - {message}: {values_str}')


log(1, 'Favorites', 7, 33)      # New with *args OK
log(1, 'Hi there')              # New message only OK
log('Favorite numbers', 7, 33)  # Old usage breaks


# To avoid this possibility entirely, you should use keyword-only arguments
# when you want to extend functions that accept *args
# To be even more defensive, you could also consider using type annotations

# Item 23: Provide Optional Behavior with Keyword Arguments
# All normal arguments to Python functions can also be passed by keyword,
# where the name of the argument is used in an assignment within the parentheses of a function call.
# The keyword arguments can be passed in any order
# as long as all the required positional arguments are specified.
# You can mix and match keyword and positional arguments.
def remainder(number, divisor):
    return number % divisor


assert remainder(20, 7) == 6
remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)
# remainder(number=20, 7)  # Positional arguments must be specified before keyword arguments.
remainder(20, number=7)  # Each argument can be specified only once.


# If you already have a dictionary, and you want to use its contents to call a function like remainder,
# you can do this by using the ** operator.
# This instructs Python to pass the values from the dictionary
# as the corresponding keyword arguments of the function
my_kwargs = {
    'number': 20,
    'divisor': 7,
}
assert remainder(**my_kwargs) == 6

# You can mix the ** operator with positional arguments or keyword
# arguments in the function call, as long as no argument is repeated
my_kwargs = {
    'divisor': 7,
}
assert remainder(number=20, **my_kwargs) == 6

# You can also use the ** operator multiple times
# if you know that the dictionaries don’t contain overlapping keys
my_kwargs = {
    'number': 20,
}
other_kwargs = {
    'divisor': 7,
}
assert remainder(**my_kwargs, **other_kwargs) == 6


# And if you’d like for a function to receive any named keyword argument,
# you can use the **kwargs catch-all parameter to collect those arguments
# into a dict that you can then process
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')


print_parameters(alpha=1.5, beta=9, gamma=4)

# The first benefit is that keyword arguments make the function call clearer
# to new readers of the code.
# The second benefit of keyword arguments is that
# they can have default values specified in the function definition.
# This works well for simple default values;
# it gets tricky for complex default values
# The third reason to use keyword arguments is that they provide a powerful way
# to extend a function’s parameters
# while remaining backward compatible with existing callers.
# The best practice is to always specify optional arguments using the keyword
# names and never pass them as positional arguments.

# Item 24: Use None and Docstrings to Specify Dynamic Default Arguments
# Sometimes you need to use a non-static type as a keyword argument’s default value.
# For example, say I want to print logging messages
# that are marked with the time of the logged event.
from time import sleep
from datetime import datetime


# This does not work as expected.
# The timestamps are the same because datetime.now is executed only a single time:
# when the function is defined.
# This can cause odd behaviors for dynamic values (like {}, [], or datetime.now())
def log(message, when=datetime.now()):
    print(f'{when}: {message}')


log('Hi there!')
sleep(0.1)
log('Hello again!')


# The convention for achieving the desired result in Python is to provide a default value of None
# and to document the actual behavior in the docstring
# When your code sees the argument value None, you allocate the default value accordingly
def log(message, when=None):
    """Log a message with a timestamp.
    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
"""
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')


log('Hi there!')
sleep(0.1)
log('Hello again!')

# Using None for default argument values is especially important
# when the arguments are mutable.
# For example, say that I want to load a value encoded as JSON data;
# if decoding the data fails, I want an empty dictionary to be returned by default
import json


# The problem here is the same as in the datetime.now example above.
# The dictionary specified for default will be shared by all calls to
# decode because default argument values are evaluated only once
# (at module load time).
def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default


foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)
assert foo is bar


# The fix is to set the keyword argument default value to None and then
# document the behavior in the function’s docstring
def decode(data, default=None):
    """Load JSON data from a string.
    Args:
        data: JSON data to decode.
        default: Value to return if decoding fails.
            Defaults to an empty dictionary.
"""
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
        return default


foo = decode('bad data')
foo['stuff'] = 5
bar = decode('also bad')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)
assert foo is not bar

# This approach also works with type annotations
from typing import Optional


def log_typed(message: str,
              when: Optional[datetime] = None) -> None:
    """Log a message with a timestamp.
    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
"""
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')


# Item 25: Enforce Clarity with Keyword-Only and Positional-Only Arguments
# For example, say I want to divide one number by another but know that I need to be very careful about special cases.
# Sometimes, I want to ignore ZeroDivisionError exceptions and return infinity instead.
# Other times, I want to ignore OverflowError exceptions and return zero instead

# With complex functions like this, it’s better to require that callers are clear about their intentions
# by defining functions with keyword-only arguments.
# These arguments can only be supplied by keyword, never by position.
# The * symbol in the argument list indicates the end of positional arguments
# and the beginning of keyword-only arguments.
def safe_division(number, divisor, *,
                  ignore_overflow=False,
                  ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


result = safe_division(1.0, 0, ignore_zero_division=True)
assert result == float('inf')
try:
    result = safe_division(1.0, 0)
except ZeroDivisionError:
    pass  # Expected


# Positional-only arguments is the opposite of the keyword-only arguments demonstrated above.
# These arguments can be supplied only by position and never by keyword.
# The / symbol in the argument list indicates where positional-only arguments end
def safe_division(numerator, denominator, /, *,  # Changed
                  ignore_overflow=False,
                  ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


assert safe_division(2, 5) == 0.4


# One notable consequence of keyword- and positional-only arguments is
# that any parameter name between the / and * symbols in the argument list may be passed
# either by position or by keyword
# (which is the default for all function arguments in Python).
# Depending on your API’s style and needs,
# allowing both argument passing styles can increase readability and reduce noise.
# For example, here I’ve added another optional parameter to safe_division
# that allows callers to specify how many digits to use in rounding the result
def safe_division(numerator, denominator, /,
                  ndigits=10, *,
                  ignore_overflow=False,
                  ignore_zero_division=False):
    try:
        fraction = numerator / denominator
        return round(fraction, ndigits)
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else: raise


result = safe_division(22, 7)
print(result)
result = safe_division(22, 7, 5)
print(result)
result = safe_division(22, 7, ndigits=2)
print(result)


# Item 26: Define Function Decorators with functools.wraps
# Python has special syntax for decorators that can be applied to functions.
# A decorator has the ability to run additional code before and after each call
# to a function it wraps.
# This means decorators can access and modify input arguments, return values, and raised exceptions.
# This functionality can be useful
# for enforcing semantics, debugging, registering functions, and more.

# For example, say that I want to print the arguments and return value of a function call.
# This can be especially helpful when debugging
# the stack of nested function calls from a recursive function.

# I define such a decorator by using *args and **kwargs
# to pass through all parameters to the wrapped function
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result
    return wrapper


# I can apply this decorator to a function by using the @ symbol
# Using the @ symbol is equivalent to calling the decorator on the function it wraps
# and assigning the return value to the original name in the same scope: fibonacci = trace(fibonacci)
@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))


fibonacci(4)

# This works well, but it has an unintended side effect.
# The value returned by the decorator—the function that’s called above—does not think it’s named fibonacci
print(fibonacci)

# The cause of this isn’t hard to see.
# The trace function returns the wrapper defined within its body.
# The wrapper function is what’s assigned to the fibonacci name in the containing module
# because of the decorator.

# This behavior is problematic because it undermines tools
# that do introspection, such as debuggers
# For example, the help built-in function is useless when called on the decorated fibonacci function.
# It should instead print out the doc- string defined above ('Return the n-th Fibonacci number')
# Object serializers break because they can’t determine the location of the original function that was decorated
import pickle

pickle.dumps(fibonacci)


# The solution is to use the wraps helper function from the functools built-in module.
# This is a decorator that helps you write decorators.
# When you apply it to the wrapper function,
# it copies all the important metadata about the inner function to the outer function
from functools import wraps


def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ...
    return wrapper


@trace
def fibonacci(n):
    ...


help(fibonacci)
print(pickle.dumps(fibonacci))

# Beyond these examples, Python functions have many other standard attributes
# (e.g., __name__, __module__, __annotations__) that must be preserved
# to maintain the interface of functions in the language.
# Using wraps ensures that you’ll always get the correct behavior.
