import psutil
import os


class BigDataResultSet(object):

    def __init__(self, id, tablename, kls, qb):
        self._id = id
        self.table_name = tablename
        self.set_label = id+' '+str(self.__class__)
        self.results = list()
        self._index = 0
        self.kls = kls
        self.sql = """ select * from %s """ % (self.table_name)
        self.where_count = 0
        self.qb = qb
        self.batch = 0
        self.batch_size = 100
        self.tlimit = 100000
        self.cumulative = 0
        self.__load_next()
        self.debug = False

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.results)

    def __load_next(self, start=0):
        self.results = []
        sql = self.qb.query+' LIMIT '+str(start)+','+str(self.batch_size)+';'
        results = self.kls.env.execute(sql)
        for g in results:
            r = self.kls()
            for k in g:
                r.set_initial_data(k, g[k])
                setattr(r, k, g[k])
            self.add_row(r)

    def set_batch_size(self, s):
        self.batch_size = s

    def add_row(self, row):
        self.results.append(row)

    def __next__(self):
        if self._index < len(self.results):
            result = self.results[self._index]
            self._index += 1
            self.cumulative += 1
            return result
        elif self.cumulative < self.tlimit:
            self.batch += 1
            if self.debug is True:
                jj = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
                print('#######################################')
                print('####    batch %s         %s   ####' %
                      (str(self.batch), str(jj)))
                print('#######################################')
            bstart = self.batch_size * self.batch
            self.__load_next(start=bstart)
            if len(self.results) == 0:
                self._index = 0
                raise StopIteration
            self._index = 0
            result = self.results[self._index]
            self._index += 1
            return result
        else:
            self._index = 0
            raise StopIteration
