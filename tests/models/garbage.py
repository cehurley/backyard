from backyard import Model


class Garbage(Model):
    __tablename__ = 'garbage_1111'
    __primary_key__ = 'id'
    belongs_to = {'user': {'fk': 'user_id', 'class': 'User'}}
