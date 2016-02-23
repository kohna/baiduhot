# __author__ = 'kohna'
# -*- coding:UTF-8 -*-
import requests
import sqlite3
import time
import re


class DBopt:
    def __init__(self):
        try:
            self.dbcon = sqlite3.connect('hot.db3')
        except sqlite3.Error, e:
            print "error 01"
            return

        self.dbcur = self.dbcon.cursor()
        self.sql = 'sql'

    def sqlexe(self):
        try:
            temp = self.dbcur.execute(self.sql)
        except sqlite3.Error, e:
            print "error 02"
            return
        self.dbcon.commit()

        return temp

    def dbclose(self):
        self.dbcon.close()


db = DBopt()
db.sql = '''CREATE TABLE IF NOT EXISTS hotid(id INTEGER PRIMARY KEY,b INTEGER ,title VARCHAR(32),url VARCHAR(64), cloc TIME )'''
db.sqlexe()
cloc = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
timest = str(time.time())
for i in range(1, 10000):
    url = 'http://top.baidu.com/clip?b=' + str(i)
    rtex = requests.get(url)
    if len(rtex.content) != 32283:
        tre = re.findall("\[\"p_name\"\] = \".*?\"", rtex.content)
        titl = tre[0][14:-1].decode('GBK')
        print titl
        db.sql = "INSERT INTO hotid(b,title,url,cloc) VALUES (" + str(i) + ",'" + titl + "','" + url + "','" + cloc + "')"
        db.sqlexe()
    time.sleep(2)
db.dbclose()
