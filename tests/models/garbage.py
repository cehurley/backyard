from tinyorm import Model

class Garbage(Model):
    __tablename__ = 'garbage'
    __primary_key__ = 'id'
