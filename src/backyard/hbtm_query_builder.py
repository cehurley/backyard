from .exceptions import TooManyLimitClauses
from .exceptions import TooManyWhereClauses
from .exceptions import TooManyOrderByClauses


class HBTMQueryBuilder(object):

    def __init__(self, func):
        self.query = ''
        self.fields_s = '*'
        self.where_s = ''
        self.tablename = None
        self.joiner = None
        self.pk = None
        self.target_fk = None
        self.fk = None
        self.fk_val = None
        self.limit_s = ''
        self.limit_count = 0
        self.where_count = 0
        self.order_s = ''
        self.order_count = 0
        self.callback = func

    def fields(self, fields):
        self.fields_s = ','.join(fields)
        return self

    def where(self, condition):
        if self.where_count > 0:
            raise TooManyWhereClauses
        if condition is not None and condition.strip() != '':
            self.where_s = " where "
            self.where_s += " %s " % condition
            self.where_count += 1
        return self

    def order(self, condition):
        if self.order_count > 0:
            raise TooManyOrderByClauses
        self.order_s = " ORDER BY "
        self.order_s += " %s " % condition
        self.order_count += 1
        return self

    def limit(self, condition):
        if self.limit_count > 0:
            raise TooManyLimitClauses
        self.limit_s = " LIMIT "
        if isinstance(condition, (list, tuple)):
            condition = ','.join(condition)
        else:
            pass
        self.limit_s += " %s " % str(condition)
        self.limit_count += 1
        return self.all()

    def all(self):
        q = 'SELECT '+self.fields_s+' FROM '+self.tablename+' '+self.where_s
        if self.where_s == '':
            q += " where "
        else:
            q += " and "
        q += self.pk + " in (select " + str(self.target_fk) + " from " + self.joiner\
            + " where " + self.fk + " = " + str(self.fk_val) + ")"
        q += ' '+self.order_s+' '+self.limit_s+';'
        self.query = q
        print(q)
        return self.callback(self)
