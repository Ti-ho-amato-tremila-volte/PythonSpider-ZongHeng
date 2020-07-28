# -*- coding:utf-8 -*-
# @Time :2020/7/24 1:40
# @Author:Ti-ho-amato-tremila-volte
# @File : wordcloud.py
# @Software: PyCharm
import jieba  # 分词
from matplotlib import pyplot as plt    # 绘图，数据可视化
from wordcloud import WordCloud         # 词云
from PIL import Image                   # 图片处理
import numpy as np                        # 矩阵运算
import sqlite3

# 词云分析——author.db作者姓名

# 准备词云所需要的词

def getData():
    author_name = []

    con = sqlite3.connect("ZongHengYuePiao.db")
    cur = con.cursor()
    sql_2 = "select * from ZongHengYuePiao"
    data_2 = cur.execute(sql_2)
    for i in data_2:
        author_name.append(i[3])
    cur.close()
    con.close()

    con1 = sqlite3.connect("ZongHeng24hour.db")
    cur1 = con1.cursor()
    sql2_2 = "select * from ZongHeng24hour"
    data2_2 = cur1.execute(sql2_2)
    for i in data2_2:
        author_name.append(i[2])
    cur1.close()
    con1.close()

    con = sqlite3.connect("ZongHengTuiJian.db")
    cur = con.cursor()
    sql3_2 = "select * from ZongHengTuiJian"
    data3_2 = cur.execute(sql3_2)
    for i in data3_2:
        author_name.append(i[3])
    cur.close()
    con.close()

    con = sqlite3.connect("ZongHengDianJi.db")
    cur = con.cursor()
    sql4 = "select * from ZongHengDianJi"
    data4 = cur.execute(sql4)
    for i in data4:
        author_name.append(i[3])
    cur.close()
    con.close()

    con = sqlite3.connect("ZongHengXinShu.db")
    cur = con.cursor()
    sql5 = "select * from ZongHengXinShu"
    data5 = cur.execute(sql5)
    for i in data5:
        author_name.append(i[3])

    cur.close()
    con.close()

    return author_name


text = ""
result = getData()
for i in result:
    text += i
# print(text)

# 分词
cut = jieba.cut(text)
string = ' '.join(cut)
print(string)
#
# 生成遮罩图片
img = Image.open(r"static\images\panda1.jpg")
img_array = np.array(img)  # 将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path='FZSTK.TTF',  # 字体
)
wc.generate_from_text(string)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')  # 是否显示坐标轴
#
# plt.show()
plt.savefig("wordcloud.jpg", dpi=1080)
