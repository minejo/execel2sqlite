#!/usr/bin/env python
#-*- coding: utf-8 -*-
###   Author: Jonathan Li<jonathan.swjtu@gmail.com>  ###
import xlrd
import sqlite3
import xdrlib,sys
import os

def main():
    print('input the output sqlite database file name:')
    sqlfile = input()
    con = sqlite3.connect(sqlfile + '.db')
    c = con.cursor()
    createsql = 'create table ' + sqlfile + """  (
        name text, 
        gender text,
        birthday text,
        age integer)"""
    c.execute(createsql)
#需要批量导入的excel的目录中的文件列表
    exceldir = '/home/li/Documents/testexcel'
    listfile = os.listdir(exceldir)
    for file in listfile:
        #依次导入每个excel文件的数据
        edata = xlrd.open_workbook(os.path.join(exceldir,file))
        #使用excel的第一个sheet
        table = edata.sheets()[0]
        nrow = table.nrows
        n = 1
        while n < nrow:
            rowdata = table.row_values(n)
            #删除第一列的序号
            del rowdata[0]
            n = n + 1
            c.execute('insert into ' + sqlfile + ' values (?,?,?,?)', rowdata)
    con.commit()
    c.close()

if __name__=="__main__":
    main()
