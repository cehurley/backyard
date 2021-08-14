import backyard
from driver_models import *

u = User.get().where(" first_name = 'hhhh' ").all()
for g in u:
    g.load('garbages')
    print(g.json())
    print(g.check_state())
    g.first_name = 'asdadasdasdads'
    print(g.check_state())
    g.first_name = 'hhhh'
    print(g.check_state())

u = User.new()
u.first_name = 'asdadasdasd'
u.save()
print(u.json())
