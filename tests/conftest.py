from .models import User, Garbage, Truck
from backyard import Env
from dotenv import dotenv_values
from .pretest import usertable, garbagetable, teardown
from .pretest import userdata, garbagedata
from .pretest import garbagetruckstable, truckstable
from .pretest import garbagetrucksdata, trucksdata
import pymysql


config = dotenv_values(".env")
env = Env(config)

for m in (User, Garbage, Truck):
    m.bind(env)

print('installing test data')


def pytest_sessionstart(session):
    for i in teardown:
        env._test_func(i)
    sql = usertable
    env._test_func(sql)
    sql = garbagetable
    env._test_func(sql)
    sql = garbagetruckstable
    env._test_func(sql)
    sql = truckstable
    env._test_func(sql)
    for r in userdata:
        env._test_func(r)
    for j in garbagedata:
        env._test_func(j)
    for j in garbagetrucksdata:
        env._test_func(j)
    for j in trucksdata:
        env._test_func(j)


def pytest_sessionfinish(session, exitstatus):
    '''
    env.close()
    from .pretest import teardown
    conn = pymysql.connect(host=config['HOST'],
                           port=int(config['PORT']),
                           user=config['USER'],
                           passwd=config['PASSWORD'],
                           db=config['DB'],
                           charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    for i in teardown:
        print(i)
        cursor.execute(i)
    conn.commit()
    conn.close()
    '''
    pass
