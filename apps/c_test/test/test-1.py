
from rest_framework import serializers

instance = {}

def get_instance(a_class, *args):
    if a_class not in instance:
        instan = a_class(*args)
        instance[a_class] = instan
        return instan

    return instance[a_class]

def singleton(a_class, *args):
    def on_call(*args):
        return get_instance(a_class, *args)

    return on_call

@singleton
class Person:
    def __init__(self, age):
        self.age = age


a = Person(3)
b = Person()

print(a.age)
print(b.age)

class A(serializers.ModelSerializer):
    pass

a = A()
a.save()
