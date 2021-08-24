import pymysql
import json


class MySQLProvider(object):
    def __init__(self, config):
        self.conn = pymysql.connect(host=config['HOST'],
                                    port=int(config['PORT']),
                                    user=config['USER'],
                                    passwd=config['PASSWORD'],
                                    db=config['DB'],
                                    charset='utf8')
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.config = config

    def execute(self, sql, data={}):
        self.cursor.execute(sql, data)
        rv = self.cursor.fetchall()
        return rv

    def insert(self, sql, data={}):
        self.cursor.execute(sql, data)
        self.conn.commit()
        rv = self.cursor.lastrowid
        return rv

    def update(self, sql, data={}):
        self.cursor.execute(sql, data)
        self.conn.commit()

    def getOne(self, sql, data):
        self.cursor.execute(sql, data)
        rv = self.cursor.fetchone()
        return rv

    def get_headersOLD(self, tablename):
        sql = """select * from %s limit 1""" % (tablename)
        self.cursor.execute(sql)
        row_headers = [x[0] for x in self.cursor.description]
        return row_headers

    def get_headers(self, tablename):
        sql = """ SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = '%s' AND
                    TABLE_NAME = '%s'; """ % (self.config['DB'], tablename)
        self.cursor.execute(sql)
        rv = self.cursor.fetchall()
        return rv

    def describe_table(self, tablename):
        sql = """ describe %s; """ % (tablename)
        self.cursor.execute(sql)
        rv = self.cursor.fetchall()
        return rv

    def delete(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def _test_func(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return 1

    def close(self):
        self.conn.close()

    def hbtm(self, tablename, joiner, pk,  pk_val):
        sql = """
                select g.* from `{0}` g
                where g.id in (select {1} from {2}
                where truck_id = {pk_val});
                """.format(tablename, pk, joiner, pk_val)
        self.cursor.execute(sql)
        rv = self.cursor.fetchall()
        return rv
