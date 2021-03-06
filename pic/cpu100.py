import random
from json import dumps

s = []
c = []
for i in range(100):
    s.append(random.uniform(95.5, 100.0))
    c.append(random.uniform(31.5, 65.4))

print(dumps(s))
print(dumps(c))