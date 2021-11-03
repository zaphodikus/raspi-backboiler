import sqlite3 as sql
import datetime, time
import os

class DbBaseObject(object):
    """
    Wrapper/helper object for a record
    """
    def __init__(self, connection, tablename, fields, clear=False):
        self.con = connection
        cursorObj = connection.cursor()
        self.tablename = tablename
        self.fields = fields
        if clear:
            _clear_qry = f"drop table if exists {self.tablename}"
            cursorObj.execute(_clear_qry)
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


class DbSensorDatabase(object):
    """
    Sensor object Table management
    """
    db_timeformat = "%Y-%m-%d %H:%M:%S"  # hard coded system time formatter
    db_sensor_stale_time = 10            # seconds before we decide data has not arrived

    def __init__(self, db_root_path='../db', drop=True):
        print(f"SQLite version {sql.sqlite_version}")
        print(f"Opening {os.path.join(db_root_path, 'dbaccess')}")
        conn = sql.connect(os.path.join(db_root_path, 'dbaccess'))

        cursorObj = conn.cursor()
        if drop:
            cursorObj.execute('drop table if exists sensors')
        self.con = conn

    def get_connection(self):
        return self.con


class DbSensor(DbBaseObject):
    """
    Temp sensor. Might be generalized for other sensors in future
    """
    # database field convenient names
    LAST_VALUE = 'last_value'
    LAST_LIVE = 'last_live'
    DISPLAY_NAME = 'display_name'
    SENSOR_ADDRESS = 'address'
    def __init__(self, connection, source:str, address: str):
        fields = [
            f"{self.SENSOR_ADDRESS} text PRIMARY KEY",
            "source text",
            f"{self.DISPLAY_NAME} text",
            f"{self.LAST_VALUE} real",
            f"{self.LAST_LIVE} text",
            f"unit text"
        ]
        super().__init__(connection, 'sensors', fields)
        self.address = address
        try:
            self.get()
        except Exception as e:
            self._create_row([f"{address}", f"{source}", f"unknown-{address}", 0.0, '', r"°C"])

    def _row_dict(self, row:[]):
        d = dict(zip(self._field_names(), row))
        return d

    def get(self):
        row = self._read_row_where(key=self.SENSOR_ADDRESS, value=self.address)
        if row is None:
            raise Exception(f"No matching address '{self.address}'!")
        return self._row_dict(row)

    def set(self, value=None, name=None):
        values = {}
        if value is not None:
            values[self.LAST_VALUE] = value
            # write a current timestamp
            values[self.LAST_LIVE] = datetime.datetime.now().strftime(DbSensorDatabase.db_timeformat)
        if name is not None:
            values[self.DISPLAY_NAME] = name
        self._write_row_where(key=self.SENSOR_ADDRESS, value=self.address, values=values)

    def stale(self):
        row = self.get()
        age = datetime.datetime.now() - datetime.datetime.strptime(row[self.LAST_LIVE], DbSensorDatabase.db_timeformat)
        return age.total_seconds() > DbSensorDatabase.db_sensor_stale_time


class DbDS18B20Sensor(DbSensor):
    def __init__(self, connection, address):
        super().__init__(connection, 'DS18B20', address)


class DbMAX6675Sensor(DbSensor):
    def __init__(self, connection, address):
        super().__init__(connection, 'MAX6675', address)


if __name__ == "__main__":
    db = DbSensorDatabase()
    sensors = []
    for i in range(0, 6):
        sensors.append( DbDS18B20Sensor(db.get_connection(), str(i)))
        sensors[i].set(name=f"Sensor:{i}")
    for n in range(0, 9):
        for i in range(0, 6):
            sensors[i].set(i)
            sensors[i].get()
            print(str(sensors[i].get()) + ' ' + str(sensors[i].stale()))
        time.sleep(0.01)
