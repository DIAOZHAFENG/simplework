# -*- coding: utf-8 -*-
import json
import pymssql
from DBUtils.PooledDB import PooledDB

with open('db_settings', 'r') as sf:
    s = json.load(sf)


class MSSQL:
    # 连接池对象
    __pool = None

    def __init__(self):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        self._conn = MSSQL.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if MSSQL.__pool is None:
            __pool = PooledDB(creator=pymssql, mincached=4, maxcached=20,
                              host=s['host'], user=s['user'], password=s['pwd'], database=s['db'])
        return __pool.connection()

    def query(self, sql):
        self._cursor.execute(sql)
        res_list = self._cursor.fetchall()
        self._conn.close()
        return res_list

    def query_itr(self, sql):
        self._cursor.execute(sql)
        while True:
            row = self._cursor.fetchone()
            if row:
                yield row
            else:
                break
        self._conn.close()

    def execute(self, sql):
        # print sql
        self._cursor.execute(sql)
        self._conn.commit()
        self._conn.close()
