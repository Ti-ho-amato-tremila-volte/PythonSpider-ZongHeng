# -*- coding:utf-8 -*-
# @Time :2020/7/22 9:45
# @Author:Ti-ho-amato-tremila-volte
# @File : zongHeng.py
# @Software: PyCharm
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3


# 爬虫——纵横中文网http://www.zongheng.com/rank.html月票榜、新书榜、点击榜、24小时更新榜、推荐榜

# 1.请求网页
def askUrl(url):
    # 用户代理
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40"}
    req = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
        # print(html)
    except Exception as e:
        if hasattr(e, "code"):
            print(e, "code")
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 2.数据获取规则——正则表达式
# 月票数、人气数、点击数等
findTicket = re.compile(r'<div class="rank_d_b_ticket">(\d*)<span>')
# 小说名
findName = re.compile(r'<div class="rank_d_b_name" title="(.*)">')
# 作者
findAuthor = re.compile(r'<div class="rank_d_b_cate" title="(.*)">')
# 类型
findGenres = re.compile('\|<a target="_blank">(.*)</a>\|')
# 状态
# infomation
findInfo = re.compile(r'<div class="rank_d_b_info">(.*?)</div>', re.S)
# 最新章节
findNew = re.compile(r'<div class="rank_d_b_last" title="(.*?)">')
# 更新日期
findUpdate = re.compile(r'<span class="rank_d_b_time">(.*?)</span>')


# 小说链接
# 图片链接
# 3.获取数据(可以获取任意榜单数据)
def getData(baseUrl):
    bookList = []
    for i in range(0, 10):
        url = baseUrl + str(i + 1)
        html = askUrl(url)
        # print(html)
        x = 0
        bs = BeautifulSoup(html, "html.parser")
        for item in bs.find_all('div', class_="rank_d_list borderB_c_dsh clearfix"):
            # print(item)
            book = []
            item = str(item)
            # 月票数、点击数等
            book_ticket = re.findall(findTicket, item)[0]
            # print(book_ticket)
            book.append(book_ticket)
            # 小说名
            book_name = re.findall(findName, item)[0]
            book.append(book_name)
            # print(book_name)
            # 作者
            book_author = re.findall(findAuthor, item)[0]
            book.append(book_author)
            # print(book_author)
            # print(book)
            # 小说类型
            book_genres = re.findall(findGenres, item)[0]
            book.append(book_genres)
            # print(book_genres)
            # 小说信息
# 特殊方法获取数据
            div = []
            book_author = bs.select(".rank_d_book_intro.fl>.rank_d_b_cate>a")  # 作者信息链接
            for link in book_author:
                # print(link.text)
                div.append(str(link.text))
            # print(div)
            for i in range(0, 20):
                del div[i]
                del div[i]
            book.append(div[x])

            # print(book)
            # book_status = re.findall(findStatus, item)
            # print(book_status)
            # 简介信息
            book_info = re.findall(findInfo, item)
            if len(book_info) != 0:
                book_info = book_info[0].replace("。", "")
                book.append(book_info)
            else:
                book.append(" ")
            # print(book_info)
            # 最新章节
            book_new = re.findall(findNew, item)
            # print(book_new)
            if len(book_new) == 0:
                book.append(" ")
            else:
                book.append(book_new[0])
            # 更新日期
            book_update = re.findall(findUpdate, item)[0]
            # print(book_update)
            book.append(book_update)
            # 小说链接
            # book_link = re.findall(findLink, item)
            # print(book_link)
# 特殊方法获取数据
            div_2 = []
            book_link = bs.select(".rank_d_b_name>a")
            for link in book_link:
                div_2.append(link["href"])
            book.append(div_2[x])

            # 图片链接
            # book_img = re.compile(findImgInfo, item)
            # print(book_img)
# 特殊方法获取数据
            div_3 = []
            book_img = bs.select(".rank_d_book_img.fl>a>img")  # 封面链接
            for link in book_img:
                div_3.append(link["src"])
            book.append(div_3[x])
            x += 1
            # print(book)
            bookList.append(book)

    return bookList


# 处理获得的数据
def getData1(baseUrl):
    bookList = []
    for i in range(0, 15):
        url = baseUrl + str(i + 1)
        html = askUrl(url)
        # print(html)
        x = 0
        bs = BeautifulSoup(html, "html.parser")
        for item in bs.find_all('div', class_="rank_d_list borderB_c_dsh clearfix"):
            # print(item)
            book = []
            item = str(item)
            # 小说名
            book_name = re.findall(findName, item)[0]
            book.append(book_name)
            # print(book_name)
            # 作者
            book_author = re.findall(findAuthor, item)[0]
            book.append(book_author)
            # print(book_author)
            # print(book)
            # 小说类型
            book_genres = re.findall(findGenres, item)[0]
            book.append(book_genres)
            # print(book_genres)
            # 小说信息

            div = []
            book_author = bs.select(".rank_d_book_intro.fl>.rank_d_b_cate>a")  # 作者信息链接
            for link in book_author:
                # print(link.text)
                div.append(str(link.text))
            # print(div)
            for i in range(0, 20):
                del div[i]
                del div[i]
            book.append(div[x])

            # print(book)
            # book_status = re.findall(findStatus, item)
            # print(book_status)
            # 简介信息
            book_info = re.findall(findInfo, item)
            if len(book_info) != 0:
                book_info = book_info[0].replace("。", "")
                book.append(book_info)
            else:
                book.append(" ")
            # print(book_info)
            # 最新章节
            book_new = re.findall(findNew, item)[0]
            # print(book_new)
            book.append(book_new)
            # 更新日期
            book_update = re.findall(findUpdate, item)[0]
            # print(book_update)
            book.append(book_update)
            # 小说链接
            # book_link = re.findall(findLink, item)
            # print(book_link)

            div_2 = []
            book_link = bs.select(".rank_d_b_name>a")
            for link in book_link:
                div_2.append(link["href"])
            book.append(div_2[x])

            # 图片链接
            # book_img = re.compile(findImgInfo, item)
            # print(book_img)

            div_3 = []
            book_img = bs.select(".rank_d_book_img.fl>a>img")  # 封面链接
            for link in book_img:
                div_3.append(link["src"])
            book.append(div_3[x])
            x += 1
            # print(book)
            bookList.append(book)

    return bookList


# 创建数据库--月票榜
def creatDb1(dbPath):
    # 创建数据库表
    sql = '''       
        create table ZongHengYuePiao
        (
        id Integer primary key autoincrement, 
        ticket_num Integer,
        book_name varchar,
        author varchar,
        genres varchar ,
        status varchar,
        info txt, 
        new_page txt, 
        update_date txt,
        link txt,
        pic_link txt
        )
    '''
    con = sqlite3.connect(dbPath)
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()


# 创建数据库--新书榜
def creatDb2(dbPath):
    # 创建数据库表
    sql = '''       
        create table ZongHengXinShu
        (
        id Integer primary key autoincrement, 
        peo_num Integer,
        book_name varchar,
        author varchar,
        genres varchar ,
        status varchar,
        info txt, 
        new_page txt, 
        update_date txt,
        link txt,
        pic_link txt
        )
    '''
    con = sqlite3.connect(dbPath)
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()


# 创建数据库--点击榜
def creatDb3(dbPath):
    # 创建数据库表
    sql = '''       
        create table ZongHengDianJi
        (
        id Integer primary key autoincrement, 
        click_num Integer,
        book_name varchar,
        author varchar,
        genres varchar ,
        status varchar,
        info txt, 
        new_page txt, 
        update_date txt,
        link txt,
        pic_link txt
        )
    '''
    con = sqlite3.connect(dbPath)
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()


# 创建数据库--推荐榜
def creatDb4(dbPath):
    # 创建数据库表
    sql = '''       
        create table ZongHengTuiJian
        (
        id Integer primary key autoincrement, 
        recomend_num Integer,
        book_name varchar,
        author varchar,
        genres varchar ,
        status varchar,
        info txt, 
        new_page txt, 
        update_date txt,
        link txt,
        pic_link txt
        )
    '''
    con = sqlite3.connect(dbPath)
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()


# 创建数据库--24小时榜
def creatDb5(dbPath):
    # 创建数据库表
    sql = '''       
        create table ZongHeng24hour
        (
        id Integer primary key autoincrement, 
        book_name varchar,
        author varchar,
        genres varchar ,
        status varchar,
        info txt, 
        new_page txt, 
        update_date txt,
        link txt,
        pic_link txt
        )
    '''
    con = sqlite3.connect(dbPath)
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()


# 保存到Excel-月票榜
def save2Excel(datalist1, datalist2, datalist3, datalist4, datalist5, excelPath):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)

    sheet1 = wb.add_sheet("纵横中文网小说月票榜", cell_overwrite_ok=True)
    cols1 = ("月票数", "书名", "作者", "类型", "状态", "概述", "最新章节", "更新日期", "小说链接", "封面链接")
    for i in range(0, 10):
        sheet1.write(0, i, cols1[i])
    for bookItem in range(0, 200):
        data = datalist1[bookItem]
        for j in range(0, 10):
            sheet1.write(bookItem + 1, j, data[j])

    sheet2 = wb.add_sheet("纵横中文网小说新书榜", cell_overwrite_ok=True)
    cols2 = ("人气数", "书名", "作者", "类型", "状态", "概述", "最新章节", "更新日期", "小说链接", "封面链接")
    for i in range(0, 10):
        sheet2.write(0, i, cols2[i])
    for bookItem in range(0, 200):
        data = datalist2[bookItem]
        for j in range(0, 10):
            sheet2.write(bookItem + 1, j, data[j])

    sheet3 = wb.add_sheet("纵横中文网小说点击榜", cell_overwrite_ok=True)
    cols3 = ("点击数", "书名", "作者", "类型", "状态", "概述", "最新章节", "更新日期", "小说链接", "封面链接")
    for i in range(0, 10):
        sheet3.write(0, i, cols3[i])
    for bookItem in range(0, 200):
        data = datalist3[bookItem]
        for j in range(0, 10):
            sheet3.write(bookItem + 1, j, data[j])

    sheet4 = wb.add_sheet("纵横中文网小说推荐榜", cell_overwrite_ok=True)
    cols4 = ("推荐数", "书名", "作者", "类型", "状态", "概述", "最新章节", "更新日期", "小说链接", "封面链接")
    for i in range(0, 10):
        sheet4.write(0, i, cols4[i])
    for bookItem in range(0, 200):
        data = datalist4[bookItem]
        for j in range(0, 10):
            sheet4.write(bookItem + 1, j, data[j])

    sheet5 = wb.add_sheet("纵横中文网小说24小时榜", cell_overwrite_ok=True)
    cols5 = ("书名", "作者", "类型", "状态", "概述", "最新章节", "更新日期", "小说链接", "封面链接")
    for i in range(0, 9):
        sheet5.write(0, i, cols5[i])
    for bookItem in range(0, 300):
        data = datalist5[bookItem]
        for j in range(0, 9):
            sheet5.write(bookItem + 1, j, data[j])

    wb.save(excelPath)


# 保存到SQLite--月票榜
def save2Sqlite(dataList, dbPath):
    creatDb1(dbPath)
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    for data in dataList:
        for i in range(len(data)):
            data[i] = '"' + data[i] + '"'
        sql = '''
                insert into ZongHengYuePiao(ticket_num, book_name, author, genres, status, info, new_page, update_date, link, pic_link)
                values (%s)
        ''' % ", ".join(data)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


# 保存到SQLite--新书榜
def save3Sqlite(dataList, dbPath):
    creatDb2(dbPath)
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    for data in dataList:
        for i in range(len(data)):
            data[i] = '"' + data[i] + '"'
        sql = '''
                insert into ZongHengXinShu(peo_num, book_name, author, genres, status, info, new_page, update_date, link, pic_link)
                values (%s)
        ''' % ", ".join(data)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


# 保存到SQLite--新书榜
def save4Sqlite(dataList, dbPath):
    creatDb3(dbPath)
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    for data in dataList:
        for i in range(len(data)):
            data[i] = '"' + data[i] + '"'
        sql = '''
                insert into ZongHengDianJi(click_num, book_name, author, genres, status, info, new_page, update_date, link, pic_link)
                values (%s)
        ''' % ", ".join(data)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


# 保存到SQLite--新书榜
def save5Sqlite(dataList, dbPath):
    creatDb4(dbPath)
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    for data in dataList:
        for i in range(len(data)):
            data[i] = '"' + data[i] + '"'
        sql = '''
                insert into ZongHengTuiJian(recomend_num, book_name, author, genres, status, info, new_page, update_date, link, pic_link)
                values (%s)
        ''' % ", ".join(data)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


# 保存到SQLite--24小时榜
def save6Sqlite(dataList, dbPath):
    creatDb5(dbPath)
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    for data in dataList:
        for i in range(len(data)):
            data[i] = '"' + data[i] + '"'
        sql = '''
                insert into ZongHeng24hour(book_name, author, genres, status, info, new_page, update_date, link, pic_link)
                values (%s)
        ''' % ", ".join(data)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


def main():
    url1 = r"http://www.zongheng.com/rank/details.html?rt=1&d=1&i=2&p="  # 月票榜地址
    url2 = r"http://www.zongheng.com/rank/details.html?rt=4&d=1&p="  # 新书榜地址
    url3 = r"http://www.zongheng.com/rank/details.html?rt=5&d=1&p="  # 点击榜地址
    url4 = r"http://www.zongheng.com/rank/details.html?rt=6&d=1&p="  # 推荐榜地址
    url5 = r"http://www.zongheng.com/rank/details.html?rt=10&d=1&p="  # 24小时榜
    result1 = getData(url1)  # 月票榜数据
    result2 = getData(url2)  # 新书榜数据
    result3 = getData(url3)  # 点击榜数据
    result4 = getData(url4)  # 推荐榜数据
    result5 = getData1(url5)  # 24小时榜数据
    excelPath = "纵横小说中文网五大榜.xls"  # 月票榜Excel地址

    save2Excel(result1, result2, result3, result4, result5, excelPath)  # 保存榜单数据到excel

    print("各榜单数据已保存到Excel中")
    dbPath1 = "ZongHengYuePiao.db"  # 月票榜dp
    dbPath2 = "ZongHengXinShu.db"  # 新书榜dp
    dbPath3 = "ZongHengDianJi.db"  # 点击榜dp
    dbPath4 = "ZongHengTuiJian.db"  # 推荐榜dp
    dbPath5 = "ZongHeng24hour.db"  # 24小时榜dp

    save2Sqlite(result1, dbPath1)  # 保存月票榜数据到Sqlite
    save3Sqlite(result2, dbPath2)  # 保存新书榜数据到Sqlite
    save4Sqlite(result3, dbPath3)  # 保存点击榜数据到Sqlite
    save5Sqlite(result4, dbPath4)  # 保存推荐榜数据到Sqlite
    save6Sqlite(result5, dbPath5)  # 保存24小时榜数据到Sqlite
    print("各榜单数据已保存到数据库中")


if __name__ == "__main__":
    print("开始爬取数据")
    main()
    print("数据爬取完毕")
