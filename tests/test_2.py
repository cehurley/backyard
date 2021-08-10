from .models import User, Garbage, Truck
from backyard import Env
from dotenv import dotenv_values

config = dotenv_values(".env")
env = Env(config)

for m in (User, Garbage, Truck):
    m.bind(env)


class TestCase:

    def test_load_hbtm(self):
        t = Truck.find(143)
        t.load('garbages')
        assert 'garbages' in t.json()

    def test_multi_level_hbtm(self):
        t = Truck.find(143)
        t.load('garbages')
        for j in t().garbages:
            j.load('trucks')
        assert '"trucks": [' in t.json()

    def test_load_with_conditions(self):
        t = Truck.find(143)
        t.load('garbages', conditions=" id = 144 ")
        for j in t().garbages:
            j.load('trucks')
        assert len(t().garbages) == 1


def teardown_module():
    env.close()
