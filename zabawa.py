class A:
    pass

class B(A):
    pass


a = A()
b = B()

print(isinstance(a, A))
print(type(a) == A)

print(isinstance(b, A))
print(type(b) == A)