# a circular buffer
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s19.html
#
import sqlite3 as sql
from dbaccess.sensors import DbBaseObject


class RingBuffer:
    """ class that implements a not-yet-full buffer """
    def __init__(self, size_max):
        self.max = size_max
        self.data = []

    class __Full:
        """ class that implements a full buffer """
        def append(self, x):
            """ Append an element overwriting the oldest one. """
            self.data[self.cur] = x
            self.cur = (self.cur+1) % self.max

        def get(self):
            """ return list of elements in correct order """
            return self.data[self.cur:]+self.data[:self.cur]

    def append(self, x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__Full

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data


class TableRingBuffer(DbBaseObject):
    """ class that implements a not-yet-full buffer """

    def __init__(self, conn, tablename, fields, size_max):
        self.max = size_max
        self.data = []
        super().__init__(connection=conn,
                          tablename=tablename,
                          fields=fields,
                          clear=True  # always DROP
                         )

    def insert_row(self, index, value):
        # appends a row using the index
        self._create_row([index, value])
        pass

    def update_row(self, index, value):
        # update row 'index'
        self._write_row_where('id', index, {'value': value})
        pass

    def __Full_append(self, x):
        """ Append an element overwriting the oldest one. """
        self.data[self.cur] = x
        self.update_row(self.cur, x)
        self.cur = (self.cur + 1) % self.max

    def __Full_get(self):
        """ return list of elements in correct order """
        #return self.data[self.cur:] + self.data[:self.cur]
        d = []
        for i in range(self.cur, len(self.data)):
            d.append(self._read_row_where(key='id', value=i))
        for i in range(0, self.cur):
            d.append(self._read_row_where(key='id', value=i))
        return d

    def append(self, x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        self.insert_row(len(self.data)-1, x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change from non-full to full callables
            self.append = self.__Full_append
            self.get = self.__Full_get

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        #return self.data
        d = []
        for i in range(0, len(self.data)):
            d.append(self._read_row_where(key='id', value=i))
        return d


if __name__=='__main__':
    x = RingBuffer(5)
    x.append(1); x.append(2); x.append(3); x.append(4)
    print(x.__class__, x.get())
    x.append(5)
    print(x.__class__, x.get())
    x.append(6)
    print(x.data, x.get())
    x.append(7); x.append(8); x.append(9); x.append(10)
    print(x.data, x.get())

    # ring test
    print('-'*80)
    fields = ['id text PRIMARY KEY',
              'value text']
    y = TableRingBuffer(conn=sql.connect('../db/circular'),
                        tablename='buffer',
                        fields=fields,
                        size_max=5
                        )
    y.append(1); y.append(2); y.append(3); y.append(4)
    print(y.__class__, y.get())
    y.append(5)
    print(y.__class__, y.get())
    y.append(6)
    print(y.data, y.get())
    y.append(7); y.append(8); y.append(9); y.append(10)
    print(y.data, y.get())
    y.append(11)
    print(y.data, y.get())


