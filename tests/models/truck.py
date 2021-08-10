from backyard import Model


class Truck(Model):
    __tablename__ = 'trucks_1111'
    __primary_key__ = 'id'
    hbtm = {'garbages': {'fk': 'truck_id',
                         'class': 'Garbage',
                         'through': 'garbage_trucks_1111',
                         'target_fk': 'garbage_id'}
            }
