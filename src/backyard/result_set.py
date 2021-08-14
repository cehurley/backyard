

class ResultSet(object):

    def __init__(self, id, tablename, kls):
        self._id = id
        self.table_name = tablename
        self.set_label = id+' '+str(self.__class__)
        self.results = list()
        self._index = 0
        self.kls = kls
        self.sql = """ select * from %s """ % (self.table_name)
        self.where_count = 0

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.results)

    def load(self, m):
        for q in self.results:
            if m in q.has_many:
                model = q.has_many[m]['class']
                fk = q.has_many[m]['fk']
                id = getattr(q(), q.__primary_key__)
                r = model.get().where(fk+" = "+str(id)).all()
                q.set_entity_data(m, r)
                if m not in q.loaded_rels:
                    q.loaded_rels.append(m)
        return self

    def add_row(self, row):
        self.results.append(row)

    def __next__(self):
        if self._index < len(self.results):
            result = self.results[self._index]
            self._index += 1
            return result
        self._index = 0
        raise StopIteration
