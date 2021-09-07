from . exceptions import ParseError
import copy

class ByrdFeeder(object):

    def __init__(self, filename):
        self.file = filename

class Column(object):

    def __init__(self, data):
        self.cName = data['name']
        self.type_info = data['type']
        self.size = False
        self.default = False
        self.nullable = ' DEFAULT NULL '
        self.pk = False
        self.on_update = ' ON UPDATE current_timestamp() '
        self.on_update_flag = False
        self.auto_inc = ''
        self.signed = ''
        self._parse_notation()

    def _parse_notation(self):
        t = self.type_info.split(' ')
        dt = t[0]
        if '-' in dt:
            self.size = dt.split('-')[1]
        elif dt.strip() == 'int':
            self.size = '11'
        if len(t) > 1:
            for z in t[1:]:
                if 'default' in z.lower():
                    self.default = ' DEFAULT '+z.split('=')[1]
                if z.lower() == 'r':
                    self.nullable = ' NOT NULL '
                if z.lower() == 'pk':
                    self.pk = True
                    self.nullable = ' NOT NULL '
                if z.lower() == 'auto':
                    self.auto_inc = ' AUTO_INCREMENT '
                if z.lower() == 'on_update=true':
                    self.on_update_flag = True
                if z.lower() == 'unsigned':
                    self.signed = ' unsigned '

    def render_sql(self):
        temp = "`{0}` ".format(self.cName)
        if self.size:
            temp += "{0}({1}) ".format(self.__class__.__name__.lower()[1:],
                                       self.size)
        else:
            temp += "{0} ".format(self.__class__.__name__.lower()[1:])
        temp += self.signed
        temp += self.nullable
        if self.default:
            temp += ' '+self.default
        if self.auto_inc:
            temp += self.auto_inc
        if self.on_update_flag:
            temp += self.on_update
        temp += ','
        return temp




class bInt(Column): pass
class bVarchar(Column): pass
class bFloat(Column): pass
class bDouble(Column): pass
class bBigInt(Column): pass
class bSmallInt(Column): pass
class bDecimal(Column): pass
class bTinyInt(Column): pass
class bText(Column): pass
class bBlob(Column): pass
class bTimestamp(Column): pass
class bLongText(Column): pass

type_map = {'int': bInt,
            'v': bVarchar,
            'f': bFloat,
            'd': bDouble,
            'bigint':bBigInt,
            'smallint': bSmallInt,
            'dec': bDecimal,
            'tint': bTinyInt,
            't': bText,
            'b': bBlob,
            'ts': bTimestamp,
            'lt': bLongText}

class Table(object):

    def __init__(self, data):
        self.table_name = data['table_name']
        self.attributes = data['attributes']
        self.columns_data = data['columns']
        self.columns = []
        self.data = data
        self._build()

    def _build(self):
        for c in self.columns_data:
            q = c['type'].split('-')[0].split(' ')[0]
            nc = type_map[q](c)
            self.columns.append(nc)

    def render(self):
        pk = False
        temp = '''CREATE TABLE '''
        temp += "`{0}` (\n".format(self.table_name)
        temp += "{0}\n".format(self.attributes)
        for c in self.columns:
            if c.pk:
                pk = c.cName
            temp += c.render_sql() + '\n'
        if pk:
            temp += 'PRIMARY KEY (`{0}`)'.format(pk) + '\n'
        temp += ') ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;\n'
        return temp



class TableMaker(object):

    def __init__(self, env):
        self.env = env
        self.tables = []
        self.tag = None

    def _load_file(self, filename):
        curtable = {}
        with open(filename, 'r') as q:
            for i in q:
                if '#' in i:
                    self.tag = i.strip()
                if i.strip() == '':
                    continue
                if '$' in i:
                    if 'table_name' in curtable:
                        nt = Table(copy.deepcopy(curtable))
                        self.tables.append(nt)
                    tn = i.split(':')[0][1:]
                    at = i.split(':')[1].strip()
                    curtable['table_name'] = tn
                    curtable['attributes'] = at
                    curtable['columns'] = []
                if ':' in i and '$' not in i:
                    t = i.split(':')
                    c = t[0].strip()
                    ct = t[1].strip()
                    this_column = {}
                    this_column['name'] = c
                    this_column['type'] = ct
                    curtable['columns'].append(this_column)
        if 'table_name' in curtable:
            nt = Table(copy.deepcopy(curtable))
            self.tables.append(nt)


    def parse(self, filename):
        self._load_file(filename)
        for t in self.tables:
            print(t.render())




if __name__ == '__main__':
    t = TableMaker()
    t.parse('plumbers.byrd')
