from driver_models import *
from name_gen import get_int, get_uid, get_email
from name_gen import FirstNameGen
import time


'''
namer = FirstNameGen()

for i in range(10000):
    u = User.new()
    u.first_name = namer.get_name()
    u.uid = get_uid()
    u.email = get_email()
    u.owner_id = get_int(2)
    u.created_on = time.strftime('%Y-%m-%d %H:%M:%S')
    u.save()
'''


u = User.get().limit(100)
for g in u:
    print(g.first_name, g.uid)
    #g.load('garbages')
    #print(g.json())
