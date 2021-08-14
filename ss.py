from tests.test_1 import Truck, Garbage

t = Truck.find(143)
t.load('garbages')


print(t.json())
print(len(t().garbages))

g = Garbage.new()
g().scoops = 100
g.save()
t.add(g)
print(t.json())
print(len(t().garbages))
