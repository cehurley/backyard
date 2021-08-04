from backyard import Model


class User(Model):
    __tablename__ = 'users'
    __primary_key__ = 'id'
    has_many = {'workflows': {'fk': 'owner_id', 'class': 'Workflow'}
                }
