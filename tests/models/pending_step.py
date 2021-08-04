from tinyorm import Model

class PendingStep(Model):
    __tablename__ = 'rp_steps_pending'
    __primary_key__ = 'id'
