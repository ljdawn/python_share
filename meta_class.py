#! /usr/bin/env python

import weakref

# class
class MyClass(object):
    def __new__(cls):
        print('{0}.__new__()'.format(cls.__name__))
        obj = object.__new__(cls)
        return obj
    def __init__(self):
        print('{0}.__init__()'.format(self.__class__))

class SubClass(object):
    pass

# function
def MyFun():
    print("shit")

def gen_MyFun():
    print("shit")
    def inner():
        print("damn")
    return inner

# danamic class
myclass = type("myclass", (object, ), {"__init__":lambda self:None})
# equal
class myclass(object):
    def __init__(self):
        pass

def gen_class():
    birth_hash = []

    def __new__(cls):
        obj = object.__new__(cls)
        cls.save_birth_hash(obj)
        return obj

    def __init__(self):
        pass

    def method(self):
        print(self.__class__)

    @classmethod
    def saybefore_create(cls):
        print("hi", cls)

    @classmethod
    def save_birth_hash(cls, obj):
        obj_ref = weakref.ref(obj)
        birth_hash.append(obj_ref)

    @classmethod
    def get_birth_hash(cls):
        return birth_hash

    return type("MyClass", (object, ), {"__new__":__new__,
                                        "__init__":__init__,
                                        "method":method,
                                        "saybefore_create":saybefore_create,
                                        "save_birth_hash":save_birth_hash,
                                        "get_birth_hash":get_birth_hash})


