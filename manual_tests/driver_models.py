from backyard import Model

class User(Model):
    __tablename__ = 'users_1111'
    __primary_key__ = 'id'
    has_many = {'garbages': {'fk': 'user_id', 'class': 'Garbage'}
                }

class Garbage(Model):
    __tablename__ = 'garbage_1111'
    __primary_key__ = 'id'
    belongs_to = {'user': {'fk': 'user_id', 'class': 'User'}}
    hbtm = {'trucks': {'fk': 'garbage_id',
                       'class': 'Truck',
                       'through': 'garbage_trucks_1111',
                       'target_fk': 'truck_id'}
            }
