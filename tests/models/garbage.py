from backyard import Model


class Garbage(Model):
    __tablename__ = 'garbage_1111'
    __primary_key__ = 'id'
    belongs_to = {'user': {'fk': 'user_id', 'class': 'User'}}
    has_and_belongs_to_many = {'trucks': {'fk': 'garbage_id',
                                          'class': 'Truck',
                                          'through': 'garbage_trucks_1111',
                                          'target_fk': 'truck_id'}
                               }
