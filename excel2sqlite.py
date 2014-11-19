#!/usr/bin/env python
#-*- coding: utf-8 -*-
###   Author: Jonathan Li<jonathan.swjtu@gmail.com>  ###
import xlrd
import sqlite3
import xdrlib,sys
import os

def main():
    sqlfile = "yoinfo.db"
    con = sqlite3.connect(sqlfile)
    c = con.cursor()
    createsql = """create table yoinfo(
        class integer, 
        stunum integer,
        name text,
        major text,
        field text,
        gender text,
        boss text)"""
    c.execute(createsql)
#需要批量导入的excel的目录中的文件列表
    listfile = os.listdir("/home/li/Documents/stuinfo")
    for file in listfile:
        #依次导入每个excel文件的数据
        edata = xlrd.open_workbook(os.path.join('/home/li/Documents/stuinfo',file))
        #使用excel的第一个sheet
        table = edata.sheets()[0]
        nrow = table.nrows
        n = 1
        while n < nrow:
            rowdata = table.row_values(n)
            #删除第一列的序号
            del rowdata[0]
            n = n + 1
            c.execute('insert into yoinfo values (?,?,?,?,?,?,?)', rowdata)
    con.commit()
    c.close()

if __name__=="__main__":
    main()
