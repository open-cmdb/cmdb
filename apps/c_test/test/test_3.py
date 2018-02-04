
def f(self):
    print("ffff")

d = {
    "host-name": f
}

A = type("A", (), d)

a = A()
print(a.__dir__())

getattr(a, "host-name")()