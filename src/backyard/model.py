from . hbtm_query_builder import HBTMQueryBuilder
from . has_many_query_builder import HasManyQueryBuilder
from . backyard import Env
from . backyard import Registry
from . result_set import ResultSet
import json

class Model(object):
    env = Env

    def __init__(self):
        self.__fields__ = []
        self.__entity_data__ = None
        self.__shadow__ = {}
        self.loaded_rels = []

    @classmethod
    def bind(cls, env):
        cls.env = env

    @classmethod
    def get(cls):
        qb = HasManyQueryBuilder(cls.run_query_builder)
        qb.tablename = cls.__tablename__
        return qb

    @classmethod
    def get_hbtm(cls, joiner=None, fk=None, target_fk=None, fk_val=None):
        qb = HBTMQueryBuilder(cls.run_query_builder)
        qb.tablename = cls.__tablename__
        qb.pk = cls.__primary_key__
        qb.joiner = joiner
        qb.fk = fk
        qb.target_fk = target_fk
        qb.fk_val = fk_val
        return qb

    @classmethod
    def run_query_builder(cls, qb):
        rs = ResultSet(cls.__name__, cls.__tablename__, cls)
        sql = qb.query
        results = cls.env.execute(sql)
        for g in results:
            r = cls()
            #e = EntityData()
            for k in g:
                r.set_initial_data(k, g[k])
                setattr(r, k, g[k])
            #r.insert_entity_data(e)
            rs.add_row(r)
        return rs

    @classmethod
    def find(cls, id):
        temp = cls()
        #e = EntityData()
        sql = "select * from "+cls.__tablename__
        sql += " where "+cls.__primary_key__+" = %s; "
        params = [id]
        r = cls.env.getOne(sql, params)
        for k in r:
            temp.set_initial_data(k, r[k])
            setattr(temp, k, r[k])
        #temp.insert_entity_data(e)
        return temp

    @classmethod
    def new(cls, data={}):
        temp = cls()
        c = temp.load_column_names()
        #temp.__entity_data__ = EntityData()
        for i in c:
            setattr(temp, i, None)
            temp.__shadow__[i] = None
        if len(data) > 0:
            pass
        return temp

    def resolve_class(self, k):
        q = self.__class__.__bases__[0]
        for i in q.__subclasses__():
            print(i.__name__, k)
            if i.__name__ == k:
                return i

    def __call__(self):
        pass

    def getFields(self):
        return self.__fields__

    # def insert_entity_data(self, e):
    #     self.__entity_data__ = e

    def set_field(self, f):
        self.__fields__.append(f)

    def set_initial_data(self, f, v):
        self.__fields__.append(f)
        self.__shadow__[f] = v

    def set_shadow_field(self, f, v):
        self.__shadow__[f] = v

    def set_entity_data(self, k, v):
        setattr(self, k, v)

    def rel(self, m):
        if m in self.has_many:
            model = self.has_many[m]['class']
            fk = self.has_many[m]['fk']
            id = getattr(self, self.__primary_key__)
            return model.get().where(fk+" = "+str(id)).all()
        else:
            return []

    def load(self, m, conditions=None):
        if hasattr(self, 'has_many'):
            if m in self.has_many:
                model = self.resolve_class(self.has_many[m]['class'])
                fk = self.has_many[m]['fk']
                id = getattr(self,
                             self.__primary_key__)
                r = model.get().where(fk+" = "+str(id)).all()
                self.set_entity_data(m, r)
                if m not in self.loaded_rels:
                    self.loaded_rels.append(m)
        if hasattr(self, 'hbtm'):
            if m in self.hbtm:
                model = self.resolve_class(self.hbtm[m]['class'])
                fk = self.hbtm[m]['fk']
                id = getattr(self,
                             self.__primary_key__)
                joiner = self.hbtm[m]['through']
                target_fk = self.hbtm[m]['target_fk']
                r = model.get_hbtm(joiner=joiner, fk=fk,
                                   target_fk=target_fk,
                                   fk_val=id).where(conditions).all()
                self.set_entity_data(m, r)
                if m not in self.loaded_rels:
                    self.loaded_rels.append(m)
        return self

    def check_state(self):
        state = 'CLEAN'
        temp = {}
        for i in self.__fields__:
            a = getattr(self, i)
            s = self.__shadow__[i]
            if a != s:
                temp[i] = a
        if len(temp) > 0:
            state = 'DIRTY'
        return [state, temp]

    def load_column_names(self):
        heds = self.env.get_headers(self.__tablename__)
        for i in heds:
            self.__fields__.append(i['COLUMN_NAME'])
        return self.__fields__

    @classmethod
    def show_table(cls):
        cols = cls.env.describe_table(cls.__tablename__)
        for c in cols:
            print(c)

    @classmethod
    def delete(cls, where=None):
        if where:
            j = cls._delete_query_builder(cls.__tablename__, where)
            cls.env.delete(j)

    def show_fields(self):
        return self.__fields__

    def createRecord(self):
        pass

    def reset_shadow(self, pri=None):
        for k in self.__fields__:
            self.__shadow__[k] = getattr(self, k)
        if pri:
            setattr(self, self.__primary_key__, pri)

    def dump_shadow(self):
        return self.__shadow__

    def fields(self):
        temp = []
        for i in self.__fields__:
            temp.append((i, getattr(self, i)))
        return temp

    def to_dict(self):
        temp = {}
        for i in self.__fields__:
            temp[i] = getattr(self, i)
        for j in self.loaded_rels:
            h = []
            for q in getattr(self, j):
                h.append(q.to_dict())
            temp[j] = h
        return temp

    def json(self, fields=[]):
        temp = {}
        if len(fields) > 0:
            for i in fields:
                temp[i] = getattr(self, i)
        else:
            for i in self.__fields__:
                temp[i] = getattr(self, i)
        for j in self.loaded_rels:
            h = []
            for q in getattr(self, j):
                h.append(q.to_dict())
            temp[j] = h
        return json.dumps(temp, indent=2, default=str)

    def xml(self):
        temp = '''<?xml version="1.0" encoding="UTF-8"?>\n'''
        return temp+self._xml()

    def _xml(self, space=0, ret=False):
        if space == 0:
            space = ''
        else:
            space = ' '*space
        temp = ''
        temp += '%s<%s>\n' % (space, self.__class__.__name__)
        for i in self.__fields__:
            g = getattr(self, i)
            temp += '  %s<%s>%s</%s>\n' % (space, i, g, i)
        for j in self.loaded_rels:
            temp += '  %s<%s>\n' % (space, j)
            for q in getattr(self, j):
                temp += q._xml(space=len(space)+4, ret=True)
            temp += '  %s</%s>\n' % (space, j)
        objr = '\n' if ret else ''
        temp += '%s</%s>%s' % (space, self.__class__.__name__, objr)
        return temp

    def save(self):
        x = self.check_state()
        id_set = False

        if hasattr(self, self.__primary_key__):
            id_set = getattr(self, self.__primary_key__)

        if x[0] == 'DIRTY':
            if id_set:
                j = self._update_query_builder(self.__tablename__,
                                               self.__primary_key__,
                                               getattr(self,
                                                       self.__primary_key__),
                                               x[1])

                self.env.update(j[0], j[1])
                msg = 'Record Saved'
            else:
                j = self._create_query_builder(self.__tablename__, x[1])
                x = self.env.insert(j[0], j[1])
                if x:
                    setattr(self,
                            self.__primary_key__, x)
                    self.reset_shadow()
                msg = 'Record Saved with ID: %s' % str(x)
                return msg
        else:
            msg = 'No Changes to Save'
        return msg

    @staticmethod
    def _update_query_builder(tablename, where_field, where_val,
                              update_vals={}):
        params = []
        sql = """UPDATE %s SET """ % tablename
        st = """ = %s """
        x = 0
        for k in update_vals:
            sql += k
            sql += st
            params.append(update_vals[k])
            if x < len(update_vals) - 1:
                sql += ", "
            else:
                sql += " "
            x += 1
        sql += " WHERE "
        sql += where_field
        sql += " = %s;"
        params.append(where_val)
        return [sql, params]

    @staticmethod
    def _delete_query_builder(tablename, where=' 2 = 1 '):
        '''
        Leave the funky where clause in here!
        It's to force a condition on deletes.
        '''
        sql = """ delete from %s where %s; """
        sql2 = sql % (tablename, where)
        return sql2

    @staticmethod
    def _create_query_builder(tablename, create_vals={}):
        sql = """ INSERT INTO %s (%s) VALUES (%s); """
        fh = []
        for i in create_vals:
            fh.append(i)
        f = ','.join(fh)
        vals = []
        vals2 = []
        for q in fh:
            vals.append('%s')
            vals2.append(create_vals[q])
        v = ','.join(vals)
        sql2 = sql % (tablename, f, v)
        return [sql2, vals2]

    def add(self, entity):
        return self.__add_hbtm_relation(entity)

    def __add_hbtm_relation(self, entity):
        found = 0
        if hasattr(self, 'hbtm'):
            for h in self.hbtm:
                if self.hbtm[h]['class'] == entity.__class__.__name__:
                    joiner = self.hbtm[h]['through']
                    target_fk = self.hbtm[h]['target_fk']
                    fk = self.hbtm[h]['fk']
                    plural = h
                    found = 1
        if found:
            sql = "INSERT INTO {0}".format(joiner)
            sql += " (`{0}`, `{1}`) values ".format(fk, target_fk)
            sql += "({0}, {1});".format(self.id, entity.id)
            self.env.update(sql)
            self.load(plural)
