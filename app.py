# -*- coding:utf-8 -*-
# @Time :2020/7/23 16:08
# @Author:Ti-ho-amato-tremila-volte
# @File : app.py
# @Software: PyCharm


from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_parameter
import sqlite3

app = Flask(__name__)


@app.route('/template')
def template():
    return render_template("index.html")


@app.route('/')
def index_0():
    return render_template("home.html")


@app.route('/home')
def index():
    return index_0()


@app.route('/wordcloud')
def index_2():
    return render_template("wordcloud.html")


@app.route('/analysis')
def index_3():
    #   获取纵横月票榜中小说类型及每种类型的数量
    type = []  # 类型
    num = []  # 数量
    ticket_num = []
    name_yuepiao = []
    con = sqlite3.connect("ZongHengYuePiao.db")
    cur = con.cursor()
    sql = "select genres,count(genres), sum(ticket_num) from ZongHengYuePiao group by genres"
    data = cur.execute(sql)
    for item in data:
        type.append(item[0])
        num.append(item[1])
        ticket_num.append(item[2])
    #   获取榜中所有信息（后面analysis.html页面要用到获取第一名的信息）
    sql_2 = "select * from ZongHengYuePiao"
    data_2 = cur.execute(sql_2)
    for i in data_2:
        name_yuepiao.append(i)
    cur.close()
    con.close()

    #   获取24小时更新榜中小说类型及每种类型的数量
    au = []  # 类型
    anum = []  # 数量
    name_24h = []
    con = sqlite3.connect("ZongHeng24hour.db")
    cur = con.cursor()
    sql2 = "select genres,count(genres) from ZongHeng24hour group by genres"
    data2 = cur.execute(sql2)
    for item in data2:
        au.append(item[0])
        anum.append(item[1])
    #   获取榜中所有信息（后面analysis.html页面要用到获取第一名的信息）
    sql2_2 = "select * from ZongHeng24hour"
    data2_2 = cur.execute(sql2_2)
    for i in data2_2:
        name_24h.append(i)
    cur.close()
    con.close()

    #   获取推荐榜中作者及
    # writer = []
    # wnum = []
    # con = sqlite3.connect("ZongHengTuiJian.db")
    # cur = con.cursor()
    # sql3 = "select author,count(author) from ZongHengTuiJian group by author"
    # data3 = cur.execute(sql3)
    # for i in data3:
    #     writer.append(i[0])
    #     wnum.append(i[1])
    # cur.close()
    # con.close()

    #   获取author.db中的作者姓名与每个作者出现的次数
    author_name = []
    author_num = []
    con = sqlite3.connect("author.db")
    cur = con.cursor()
    sql_3 = "select author_name,count(author_name) from author group by author_name"
    data_3 = cur.execute(sql_3)
    for i in data_3:
        author_name.append(i[0])
        author_num.append(i[1])
    cur.close()
    con.close()
    #   获取新书榜中的排名、书名、人气
    renQi = []
    id = []
    author_book_name = []
    book = []
    con = sqlite3.connect("ZongHengXinShu.db")
    cur = con.cursor()
    sql_3 = "select id, book_name, peo_num from ZongHengXinShu"
    data_3 = cur.execute(sql_3)
    for i in data_3:
        id.append(int(i[0]))
        renQi.append(int(i[2]))
        author_book_name.append(i[1])
    #   获取榜中所有信息（后面analysis.html页面要用到获取第一名的信息）
    sql_3_2 = "select * from ZongHengXinShu"
    data_3_2 = cur.execute(sql_3_2)
    for j in data_3_2:
        book.append(j)
    cur.close()
    con.close()

    return render_template("analysis.html", type=type, num=num, au=au, anum=anum,
                           name_24h=name_24h, name_yuepiao=name_yuepiao, ticket_num=ticket_num, author_name=author_name,
                           author_num=author_num, renQi=renQi, id=id, author_book_name=author_book_name, book=book)


@app.route('/team')
def index_4():
    return render_template("team.html")


@app.route('/bangdan')
def index_5():
    bookListYuePiao = []
    bookListXinShu = []
    bookListDianJi = []

    con_1 = sqlite3.connect("ZongHengYuePiao.db")
    con_2 = sqlite3.connect("ZongHengXinShu.db")
    con_3 = sqlite3.connect("ZongHengDianJi.db")

    cur_1 = con_1.cursor()
    cur_2 = con_2.cursor()
    cur_3 = con_3.cursor()
    sql_1 = "SELECT * FROM ZongHengYuePiao"
    data_yuepiao = cur_1.execute(sql_1)
    for i in data_yuepiao:
        bookListYuePiao.append(i)
    sql_2 = "SELECT * FROM ZongHengXinShu"
    data_xinshu = cur_2.execute(sql_2)
    for j in data_xinshu:
        bookListXinShu.append(j)
    sql_3 = "SELECT * FROM ZongHengDianJi"
    data_dianji = cur_3.execute(sql_3)
    for k in data_dianji:
        bookListDianJi.append(k)

    cur_1.close()
    con_1.close()
    cur_2.close()
    con_2.close()
    cur_3.close()
    con_3.close()
    return render_template("bangdan.html", bookListYuePiao=bookListYuePiao, bookListXinShu=bookListXinShu,
                           bookListDianJi=bookListDianJi)


@app.route('/yuepiao')
def index_6():
    bookList = []
    per_page = 10
    con = sqlite3.connect("ZongHengYuePiao.db")
    cur = con.cursor()
    sql = "SELECT * FROM ZongHengYuePiao"
    data = cur.execute(sql)
    for i in data:
        bookList.append(i)
    total = len(bookList)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * per_page
    end = start + per_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    book = bookList[start:end]
    context = {
        'pagination': pagination,
        'book': book
    }
    return render_template('yuepiao.html', **context)


@app.route('/xinshu')
def index_7():
    bookList = []
    per_page = 10
    con = sqlite3.connect("ZongHengXinShu.db")
    cur = con.cursor()
    sql = "SELECT * FROM ZongHengXinShu"
    data = cur.execute(sql)
    for i in data:
        bookList.append(i)
    total = len(bookList)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * per_page
    end = start + per_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    book = bookList[start:end]
    context = {
        'pagination': pagination,
        'book': book
    }
    return render_template('xinshu.html', **context)


@app.route('/dianji')
def index_8():
    bookList = []
    per_page = 10
    con = sqlite3.connect("ZongHengDianJi.db")
    cur = con.cursor()
    sql = "SELECT * FROM ZongHengDianJi"
    data = cur.execute(sql)
    for i in data:
        bookList.append(i)
    total = len(bookList)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * per_page
    end = start + per_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    book = bookList[start:end]
    context = {
        'pagination': pagination,
        'book': book
    }
    return render_template('dianji.html', **context)


@app.route('/tuijian')
def index_9():
    bookList = []
    per_page = 10
    con = sqlite3.connect("ZongHengTuiJian.db")
    cur = con.cursor()
    sql = "SELECT * FROM ZongHengTuijian"
    data = cur.execute(sql)
    for i in data:
        bookList.append(i)
    total = len(bookList)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * per_page
    end = start + per_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    book = bookList[start:end]
    context = {
        'pagination': pagination,
        'book': book
    }
    return render_template('tuijian.html', **context)


@app.route('/24hour')
def index_10():
    bookList = []
    per_page = 10
    con = sqlite3.connect("ZongHeng24hour.db")
    cur = con.cursor()
    sql = "SELECT * FROM ZongHeng24hour"
    data = cur.execute(sql)
    for i in data:
        bookList.append(i)
    total = len(bookList)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * per_page
    end = start + per_page
    pagination = Pagination(bs_version=3, page=page, total=total)
    book = bookList[start:end]
    context = {
        'pagination': pagination,
        'book': book
    }
    return render_template('24hour.html', **context)


if __name__ == '__main__':
    app.run()
