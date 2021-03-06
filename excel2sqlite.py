#!/usr/bin/env python
#-*- coding: utf-8 -*-
###   Author: Jonathan Li<jonathan.swjtu@gmail.com>  ###
import xlrd
import sqlite3
import os
import pypinyin

def convertpinyin(list):
    """convert all talbe head value from chinese to chinese pinyin and save in a list"""
    sqlfield = []
    for value in list:
        field = pypinyin.slug(value, separator = '')
        sqlfield.append(field)
    return sqlfield

def getcreatesql(sqlvaluelist, sqlfile):
    """according to the table head pinyin, we can generate the create table sql sentence"""
    allfield = ''
    ncolumn = len(sqlvaluelist)
    for covalue in sqlvaluelist:
        if sqlvaluelist.index(covalue) < ncolumn - 1:
            allfield = allfield + covalue + ' text,\n'
        else:
            allfield = allfield + covalue + ' text'
    createsql = 'create table ' + sqlfile + ' (' + allfield + ')'
    return createsql

def getinsertsql(sqlvaluelist, sqlfile):
    """generate the insert sql sentence for each data."""
    ncolumn = len(sqlvaluelist)
    insertfield = ['?'] * ncolumn
    insertsql = 'insert into ' + sqlfile + ' values (' + ','.join(insertfield) + ')'
    return insertsql

def main():
    print('input the output sqlite database file name:')
    sqlfile = input()
    con = sqlite3.connect(sqlfile + '.db')
    c = con.cursor()
   # createsql = 'create table ' + sqlfile + """  (
    #    name text,
    #    gender text,
    #    birthday text,
    #    age integer)"""
  #  c.execute(createsql)
#需要批量导入的excel的目录中的文件列表
    exceldir = '/home/li/Documents/testexcel'
    listfile = os.listdir(exceldir)
    #used to determine whether it is the first time to access an excel file.
    checkflag = 0
    for file in listfile:
        #依次导入每个excel文件的数据
        edata = xlrd.open_workbook(os.path.join(exceldir,file))
        #使用excel的第一个sheet
        table = edata.sheets()[0]
        nrow = table.nrows
        if checkflag == 0:
            columnname = table.row_values(0)
            sqlfield = convertpinyin(columnname)
            checkflag = 1
           # print(columnname)
           # print(sqlfield)
            sql = getcreatesql(sqlfield, sqlfile)
           # print(sql)
            c.execute(sql)
        n = 1
        while n < nrow:
            rowdata = table.row_values(n)
          #  del rowdata[0]
            n = n + 1
            insertsql = getinsertsql(sqlfield, sqlfile)
           # print(insertsql)
            c.execute(insertsql, rowdata)
    con.commit()
    c.close()
#save some parameter to the config file
    config = open('config', 'w')
    config.writelines('SQLname:' + sqlfile + '\n')
    config.writelines('columnvalue:' + ','.join(columnname) + '\n')
    config.writelines('sqlfield:' + ','.join(sqlfield) + '\n')
    config.close()

if __name__=="__main__":
    main()
