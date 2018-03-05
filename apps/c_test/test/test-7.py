
class Test:
    def __init__(self, age):
        self.age = age

    @property
    def get_age(self):
        return self.age

t = Test(23)
print(t.get_age)

d = {"name": "zhangsan"}
name = d.__getitem__("name")
print(name)
print(d.__dir__())