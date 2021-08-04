from backyard import Model


class Workflow(Model):
    __tablename__ = 'workflows'
    __primary_key__ = 'id'
    belongs_to = {'user': {'fk': 'user_id', 'class': 'User'}}
    has_many = {'runpacks': {'fk': 'workflow_id', 'class': 'Runpack'}
                }
