import sqlite3 as sql
from platform import python_version
import datetime, time

#import re
#import traceback

# def func(var):
#     stack = traceback.extract_stack()
#     filename, lineno, function_name, code = stack[-2]
#     vars_name = re.compile(r'\((.*?)\).*$').search(code).groups()[0]
#     print (vars_name)
#     return


db_timeformat = "%Y-%m-%d %H:%M:%S"  # hard coded system time formatter

conn = sql.connect('../db/dbaccess')
print(f'This is python version {python_version()}')
print(f"SQLite version {sql.sqlite_version}")

cursorObj = conn.cursor()

cursorObj.execute('drop table if exists sensors')
#cursorObj.execute('SELECT name from sqlite_master where type= "table"')
#print(cursorObj.fetchall())

cursorObj.execute('create table if not exists sensors(address text PRIMARY KEY, display_name text, last_value real, last_live text)')
conn.commit()
cursorObj.execute(f"insert into sensors (address, display_name, last_value, last_live ) values ('aabaaaa1', 'sensor1', 1.1, 'Y')")
conn.commit()

cursorObj.execute("SELECT * FROM sensors")
for row in cursorObj:
    print(row)

cursorObj.execute(f"update sensors set last_value = 42.1 where address = 'aabaaaa1'")
conn.commit()
cursorObj.execute("SELECT * FROM sensors")
for row in cursorObj:
    print(row)


class DbBaseObject(object):
    def __init__(self, connection, tablename, fields):
        self.con = connection
        cursorObj = connection.cursor()
        self.tablename = tablename
        self.fields = fields
        _create_qry = f"create table if not exists {self.tablename}({', '.join(self.fields)})"
        cursorObj.execute(_create_qry)
        connection.commit()

    def _field_names(self):
        return [f.split(' ')[0] for f in self.fields]

    def _create_row(self, values: []):
        assert len(self.fields) == len(values)
        cursorObj = self.con.cursor()
        insert_qry = f"insert into {self.tablename} ({', '.join(self._field_names())} ) " \
                     f"values ({','.join('?'*len(self.fields))})"
        cursorObj.execute(insert_qry, values)
        self.con.commit()

    def _read_row_where(self, key, value):
        cursorObj = self.con.cursor()
        read_qry = f"select * from {self.tablename} where {key} = ?"
        #print(f"exec: {read_qry} \n value={(value)}")
        cursorObj.execute(read_qry, [value])
        return cursorObj.fetchone()

    def _write_row_where(self, key, value, values):
        """
        update a row
        :param key: table KEY
        :param value: value of the table KEY
        :param values: may be a ordered list of all the columns data or a dict with only changed columns
        :return:
        """
        cursorObj = self.con.cursor()
        if isinstance(values, dict):
            fields = values.keys()
            values = values.values()
        else:
            fields = self._field_names()
        write_qry = f"UPDATE {self.tablename} SET {', '.join([( n + ' = ?') for n in fields])} " \
                    f"WHERE {key} = ?"
        #print(f"exec: {write_qry} \n values={[*values,value]}")
        cursorObj.execute(write_qry, [*values, value])
        self.con.commit()


class DbSensor(DbBaseObject):
    def __init__(self, connection, address: str):
        fields = [
            "address text PRIMARY KEY",
            "display_name text",
            "last_value real",
            "last_live text"
        ]
        super().__init__(connection, 'sensors', fields)
        self.address = address
        try:
            self.get()
        except Exception as e:
            self._create_row([f"{address}", f"unknown-{address}", 0.0, datetime.datetime.now().strftime(db_timeformat)])

    def get(self):
        row = self._read_row_where(key='address', value=self.address)
        if row is None:
            raise Exception(f"No matching address '{self.address}'!")
        return row

    def set(self, value=None, name=None):
        values = {}
        if value is not None:
            values['last_value'] = value
            # write a current timestamp
            values['last_live'] = datetime.datetime.now().strftime(db_timeformat)
        if name is not None:
            values['display_name'] = name
        self._write_row_where(key='address', value=self.address, values=values)

    def stale(self):
        row = self.get()
        age = datetime.datetime.now() - datetime.datetime.strptime(row[3], db_timeformat)
        return age.total_seconds()>2


cursorObj.execute('drop table if exists sensors')
sensor = DbSensor(conn, 'ababababab')
sensor.set(name="joes")
stale = False
while not stale:
    stale = sensor.stale()
    print(sensor.get())
    time.sleep(0.1)
print("stale!")
