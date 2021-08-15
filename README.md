# Backyard

# Example Usage:
~~~python
from models import User, Workflow, Runpack


if __name__ == '__main__':

    u = User.get().fields(['id','first_name','uid']).order('id asc').limit(10)
    for q in u:
        print(q.first_name)
        print(q.json())

    u = User.find(2)
    id = u.id

    u = User.find(2).load('workflows')
    for k in u.workflows:
        k.load('runpacks')
    print(u.id)
~~~

# Models
Create a 'models' folder in the root of your project
Sample model file: user.py
~~~python
from backyard import Model

class User(Model):
    __tablename__ = 'users'
    __primary_key__ = 'id'
    has_many = {'workflows':{'fk': 'owner_id', 'class': 'Workflow'}}
~~~
