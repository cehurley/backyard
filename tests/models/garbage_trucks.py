from backyard import Model


class GarbageTrucks(Model):
    __tablename__ = 'garbage_trucks_1111'
    __primary_key__ = 'id'
    belongs_to = {'trucks': {'fk': 'truck_id', 'class': 'Truck'}}
    belongs_to = {'Garbages': {'fk': 'garbage_id', 'class': 'Garbage'}}
