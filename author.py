# -*- coding:utf-8 -*-
# @Time :2020/7/23 21:51
# @Author:Ti-ho-amato-tremila-volte
# @File : author.py
# @Software: PyCharm
import sqlite3


# 统计五个榜单前十的作者

def getData():
    author_name = []

    con = sqlite3.connect("ZongHengYuePiao.db")
    cur = con.cursor()
    sql_2 = "select * from ZongHengYuePiao where id<=10"
    data_2 = cur.execute(sql_2)
    for i in data_2:
        author_name.append(i[3])
    cur.close()
    con.close()

    con1 = sqlite3.connect("ZongHeng24hour.db")
    cur1 = con1.cursor()
    sql2_2 = "select * from ZongHeng24hour where id<=10"
    data2_2 = cur1.execute(sql2_2)
    for i in data2_2:
        author_name.append(i[2])
    cur1.close()
    con1.close()

    con = sqlite3.connect("ZongHengTuiJian.db")
    cur = con.cursor()
    sql3_2 = "select * from ZongHengTuiJian where id<=10"
    data3_2 = cur.execute(sql3_2)
    for i in data3_2:
        author_name.append(i[3])
    cur.close()
    con.close()

    con = sqlite3.connect("ZongHengDianJi.db")
    cur = con.cursor()
    sql4 = "select * from ZongHengDianJi where id<=10"
    data4 = cur.execute(sql4)
    for i in data4:
        author_name.append(i[3])
    cur.close()
    con.close()

    con = sqlite3.connect("ZongHengXinShu.db")
    cur = con.cursor()
    sql5 = "select * from ZongHengXinShu where id<=10"
    data5 = cur.execute(sql5)
    for i in data5:
        author_name.append(i[3])
    cur.close()
    con.close()

    return author_name


def creatDb(dbPath):
    # 创建数据库表
    sql = '''       
        create table author
        (
        id Integer primary key autoincrement, 
        author_name varchar 
        )
    '''
    con = sqlite3.connect(dbPath)
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()


def save2Db(dataList, dbPath):
    creatDb(dbPath)
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    for data in dataList:
        data = '"' + data + '"'
        sql = '''
                insert into author(author_name)
                values (%s)
        ''' % data
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


def queruDb(dbPath):
    author_name = []
    author_num = []
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    sql3 = "select author_name, count(author_name) from author"
    data3 = cur.execute(sql3)
    for i in data3:
        author_name.append(i[0])
        author_num.append(i[1])
    cur.close()
    con.close()
    print(author_num)
    print(author_name)


def main():
    result = getData()
    # print(result)
    # for i in result:
    #     print(i)
    dbPath = "author.db"
    save2Db(result, dbPath)
    # result_2 = queruDb(dbPath)
    # print(result_2)
    # queruDb(dbPath)


if __name__ == "__main__":
    main()
