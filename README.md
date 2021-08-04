# tiny ORM

# Example Usage:
~~~python
from models import User, Workflow, Runpack
from tinyorm import Model
from tinyorm import Env
from dotenv import dotenv_values

config = dotenv_values(".env")
env = Env(config)

for m in (User, Workflow, Runpack):
    m.bind(env)

if __name__ == '__main__':
    u = User.get().fields(['id','first_name','uid']).order('id asc').limit(10)
    print('size of u: '+str(len(u)))
    for q in u:
        q.load('workflows')
        print(q.json())

    u = User.find(2).load('workflows')
    for k in u().workflows:
        k.load('runpacks')
    print(u.xml())
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
