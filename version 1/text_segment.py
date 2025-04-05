from segment import *
from node import *
n1 = Node ('aaa', 0, 0, )
n2 = Node ('bbb', 3, 4, )
n3 = Node ('ccc', 5, 7)

s1 = segment("segment 1", n1, n2)
print(s1.__dict__)

s2 = segment("segment 2", n2, n3)
print(s2.__dict__)
