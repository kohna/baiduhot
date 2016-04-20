# -*- coding:utf-8 -*-
# __author__ = 'kohna'
# Create at 2015-09-01
import re
import time
import sqlite3
import requests
import logging


mon = time.strftime('%Y%m', time.localtime())
day = time.strftime('%Y%m%d', time.localtime())
sqlDB = mon + '.db3'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename="hot.log",
                    filemode='w'
                    )


class GetHotPointList:
    def __init__(self, sb):
        self.sb = str(sb[0])
        self.senddata = '&b=' + self.sb + '&hd_h_info=1&line=20'
        self.soucdata = ''
        self.res = '.\S.\w*.:.*.]'
        self.evalres = ''
        self.sdcit = []
        self.url = "http://top.baidu.com/clip?" + self.senddata

    def getdata(self):
        try:
            self.soucdata = requests.get(self.url,timeout=10)
            reres = re.findall(self.res, self.soucdata.content)
            if len(reres) > 0:
                evalres = eval(reres[0])
                for i in evalres:
                    self.sdcit.append(i)
            else:
                logging.debug("delete url: " + self.sb)
                delbs(self.sb)
        except requests.ConnectionError, e:
            logging.debug('The Error from: + ' + str(e.args[0]))


class DBopt:
    def __init__(self, db):
        try:
            self.dbcon = sqlite3.connect(db)
        except sqlite3.Error, e:
            logging.error('Sqlit Databese error by ' + e.args[0])
            return

        self.dbcur = self.dbcon.cursor()
        self.sql = 'sql'

    def sqlexe(self):
        try:
            self.dbcur.execute(self.sql)
            self.dbcon.commit()
        except sqlite3.Error, e:
            logging.error("Sqlit3 Databese execute sql error by " + e.args[0])
            return
        return self.dbcur.fetchall()

    def dbclose(self):
        self.dbcon.close()


def checks(bx):
    dbs = DBopt("hot.db3")
    dbs.sql = "SELECT b,title FROM hotid "
    res = dbs.sqlexe()
    for tmp in list(res):
        bx.append(tmp)
    dbs.dbclose()


def delbs(b):
    dbx = DBopt("hot.db3")
    dbx.sql = "DELETE FROM hotid WHERE id=" + str(b)
    dbx.sqlexe()
    dbx.dbclose()

if __name__ == '__main__':
    bs = []
    checks(bs)
    for b in bs:
        hoy = GetHotPointList(b)
        print b[1]
        hoy.getdata()
        iui = 0
        db = DBopt(sqlDB)
        db.sql = "CREATE TABLE IF NOT EXISTS tb_" + day + "(id INTEGER PRIMARY KEY,b INTEGER,toptype VARCHAR(32),title VARCHAR(32),trend VARCHAR(32),titurl VARCHAR(64),clicks INTEGER, cloc TIME)"
        db.sqlexe()
        for ins in hoy.sdcit:
            title = hoy.sdcit[iui]['title'].decode('unicode-escape')
            trend = hoy.sdcit[iui]['trend']
            titurl = hoy.sdcit[iui]['tit_url'].replace('\\', '')
            detailurl = hoy.sdcit[iui]['detail_url']
            clicks = str(hoy.sdcit[iui]['clicks'])
            cloc = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
            db.sql = "INSERT INTO tb_" + day + "(b,title,toptype,trend,titurl,clicks,cloc) VALUES (" + str(b[0]) + ",'" + b[1] + "','" + title + "','" + trend + "','" + titurl + "','" + clicks + "','" + cloc + "')"
            db.sqlexe()
            iui += 1
        db.dbclose()
