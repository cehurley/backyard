from backyard import Model


class Truck(Model):
    __tablename__ = 'trucks_1111'
    __primary_key__ = 'id'
    has_and_belongs_to_many = {'garbages': {'fk': 'truck_id',
                                            'class': 'Garbage',
                                            'through': 'garbage_trucks_1111',
                                            'target_fk': 'garbage_id'}
                               }
