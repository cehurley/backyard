from backyard import Model


class User(Model):
    __tablename__ = 'users_1111'
    __primary_key__ = 'id'
    has_many = {'workflows': {'fk': 'owner_id', 'class': 'Workflow'}
                }
