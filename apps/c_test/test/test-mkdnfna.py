class A:
    def __init__(self):
        self._data = [1, 2]
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value



a = A()
a._data.append("lisi")
a.data.append(3)
a.data +=[4,4]

print(a.data)
print(a._data)