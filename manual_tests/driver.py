from driver_models import User
from name_gen import get_int, get_uid, get_email
from name_gen import FirstNameGen
import tracemalloc
import psutil
import os
import time
'''
namer = FirstNameGen()

for i in range(100000):
    u = User.new()
    u.first_name = namer.get_name()
    u.uid = get_uid()
    u.email = get_email()
    u.owner_id = get_int(2)
    u.created_on = time.strftime('%Y-%m-%d %H:%M:%S')
    u.save()
'''
time.sleep(15)
while 1 == 1:
    tracemalloc.start()
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    u = User.get_bigdata().order(' first_name ').all()
    u.set_batch_size(8000)
    u.debug = True
    for g in u:
        print(g.first_name, g.uid)
        #print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
        #g.load('garbages')
        #print(g.json())
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    print(tracemalloc.get_traced_memory())

    tracemalloc.stop()
    time.sleep(15)
