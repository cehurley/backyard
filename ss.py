from tests.test_1 import Truck

t = Truck.find(143)
t.load('garbages', conditions=" id = 144 ")
for j in t().garbages:
    j.load('trucks')

print(t.json())
print(len(t().garbages))
