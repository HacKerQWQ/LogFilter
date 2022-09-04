# -*- coding: utf-8 -*-
# Author: HackerQWQ
# Created Time: 1:18
import sqlite3

class db:
    def __init__(self):
        # 连接数据库
        self.con = sqlite3.connect("data.db")
        # 创建游标取数据
        cur = self.con.execute("SELECT * from sqlite_master where name='TEST'")
        # 判断数据库是否存在,不存在就创建
        if cur.fetchone() != None:
            self.clean_table()
        else:
            cur.execute('''CREATE TABLE TEST
            (ID INT PRIMARY KEY NOT NULL,
            IP TEXT NOT  NULL,
            REMOTE TEXT NOT  NULL,
            USERID TEXT NOT  NULL,
            DATE TEXT NOT  NULL,
            TIMEZONE TEXT NOT  NULL,
            METHOD TEXT NOT  NULL,
            PATH TEXT NOT  NULL,
            VERSION TEXT NOT  NULL,
            STATUS TEXT NOT  NULL,
            LENGTH TEXT NOT  NULL,
            REFERRER TEXT NOT  NULL,
            USER_AGENT TEXT NOT  NULL
            )
            ''')

            # 创建游标取数据
            cur = self.con.execute("SELECT * from sqlite_master where name='FILTER'")
            # 判断数据库是否存在,不存在就创建
            if cur.fetchone() != None:
                self.clean_table()
            else:
                cur.execute('''CREATE TABLE FILTER
                    (ID INT PRIMARY KEY NOT NULL,
                    IP TEXT NOT  NULL,
                    REMOTE TEXT NOT  NULL,
                    USERID TEXT NOT  NULL,
                    DATE TEXT NOT  NULL,
                    TIMEZONE TEXT NOT  NULL,
                    METHOD TEXT NOT  NULL,
                    PATH TEXT NOT  NULL,
                    VERSION TEXT NOT  NULL,
                    STATUS TEXT NOT  NULL,
                    LENGTH TEXT NOT  NULL,
                    REFERRER TEXT NOT  NULL,
                    USER_AGENT TEXT NOT  NULL
                    )
                    ''')

    def insert_test_data(self):
        con = self.con
        con.execute('''INSERT INTO TEST
        (ID,IP,REMOTE,USERID,DATE,TIMEZONE,METHOD,PATH,VERSION,STATUS,LENGTH,REFERRER,USER_AGENT)
        VALUES(1,"127.0.0.1","-","-","test","test","GET","/","HTTP/1.1","200","200","/","firefox")
        ''')
        con.commit()

    # id,ip,remote,userid,date,timezone,request_method,path,request_version,status,length,referrer,user_agent
    def insert_dataset(self,row):
        con = self.con
        # row = [tuple(row)]
        con.executemany('''INSERT INTO TEST
         (ID,IP,REMOTE,USERID,DATE,TIMEZONE,METHOD,PATH,VERSION,STATUS,LENGTH,REFERRER,USER_AGENT)
         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''',row)
        con.commit()

    def clean_table(self):
        con = self.con
        con.execute("delete from TEST ")
        con.execute("delete from FILTER ")
        con.commit()

    def select_data(self, condition=""):
        con = self.con
        cur = con.execute(f'''SELECT * from TEST
           WHERE 1=1 {condition}''')
        return cur.fetchall()

    def filter_data(self, condition=""):
        con = self.con
        con.execute(f'''INSERT INTO FILTER
        SELECT * from TEST
        WHERE 1=1 {condition}
        ''')
        con.commit()

    def get_filter(self):
        con = self.con
        cur = con.execute("SELECT * from FILTER")
        return cur.fetchall()

    def close(self):
        self.con.close()

    def __del__(self):
        self.close()


# test = db()
# test.insert_data()
# test.insert_dataset([(str(1),"127.0.0.1","-","-","test","test","GET","/","HTTP/1.1","200","200","/","firefox")])

