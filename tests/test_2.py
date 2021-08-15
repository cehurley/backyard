from .models import User, Truck, Garbage
from backyard import Env
from dotenv import dotenv_values

config = dotenv_values(".env")
env = Env


class TestCase:

    def test_load_hbtm(self):
        t = Truck.find(143)
        t.load('garbages')
        assert 'garbages' in t.json()

    def test_multi_level_hbtm(self):
        t = Truck.find(143)
        t.load('garbages')
        for j in t.garbages:
            j.load('trucks')
        assert '"trucks": [' in t.json()

    def test_load_with_conditions(self):
        t = Truck.find(143)
        t.load('garbages', conditions=" id = 144 ")
        for j in t.garbages:
            j.load('trucks')
        assert len(t.garbages) == 1

    def test_add_hbtm_relation(self):
        t = Truck.find(143)
        t.load('garbages')
        assert len(t.garbages) == 2
        g = Garbage.new()
        g.scoops = 100
        g.save()
        t.add(g)
        assert len(t.garbages) == 3
        #t.add(g)
        #assert len(t().garbages) == 4


def teardown_module():
    pass #env.close()
