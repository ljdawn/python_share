registry = {}

class MultiMethod(object):
    def __init__(self, name):
        self.name = name
        self.typemap = {}
    def __call__(self, *args):
        types = tuple(arg.__class__ for arg in args) # a generator expression!
        function = self.typemap.get(types)
        if function is None:
            raise TypeError("no match")
        return function(*args)
    def register(self, types, function):
        if types in self.typemap:
            raise TypeError("duplicate registration")
        self.typemap[types] = function

def multimethod(*types):
    def register(function):
        name = function.__name__
        mm = registry.get(name)
        if mm is None:
            mm = registry[name] = MultiMethod(name)
        mm.register(types, function)
        return mm
    return register

# 'overload' makes more sense in this case
overload = multimethod

class Sprite(object):
    pass

class Point(object):
    pass

class Curve(object):
    pass

@overload(Sprite, Point, Direction, int)
def add_bullet(sprite, start, direction, speed):
    # ...

@overload(Sprite, Point, Point, int, int)
def add_bullet(sprite, start, headto, speed, acceleration):
    # ...

@overload(Sprite, str)
def add_bullet(sprite, script):
    # ...

@overload(Sprite, Curve, speed)
def add_bullet(sprite, curve, speed):
    # ...
