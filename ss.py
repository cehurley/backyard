from tests.test_1 import Truck

t = Truck.find(143)
t.load('garbages')
print(t.json())
