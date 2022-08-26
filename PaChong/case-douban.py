# -*- codeng: utf-8 -*-
import re
import sqlite3
import urllib.request
import urllib.parse,urllib.error
from bs4 import BeautifulSoup
import xlwt

def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1. 爬取网页
    datalist = getData(baseurl)
    # 2. 保存数据
#    savepath = "豆瓣电影Top250.xls"
#    saveData(datalist,savepath)
    dbpath = "movie250.db"
    saveData2DB(datalist,dbpath)

# 影片详情连接的规则
findlink = re.compile(r'<a href="(.*?)">')    # compile创建正则表达式对象，表示规则（字符串的模式）
# 影片图片连接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)   # . 是不包括换行符的，所以在后面加 re.S让换行符包含在字符中
# 影片的片名
findTitile = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating =  re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 影片内容规则
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):    # 调用获取页面的函数，10次250条，页面是10页
        url = baseurl + str(i*25)
        html = askUrl(url)     # 保存获取到的网页源码
        # 逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):        # 查找符合要求的字符串，形成列表, class_ 下划线表示属性值
            data = []   # 保存一部电影的所有信息
            item =  str(item)

            link = re.findall(findlink,item)[0]      #re库用来通过正则表达式查找指定的字符串
            data.append(link)
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitile,item)     # 片名可能有中文名及外国名
            if (len(titles) == 2):
                ctitle = titles[0]                   # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/","")   # 去掉无关的符号，添加外国名
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')        # 外国名留空
            rating = re.findall(findRating,item)[0]   # 添加评分
            data.append(rating)
            findSum = re.findall(findJudge,item)[0]        # 添加评价人数
            data.append(findSum)
            inq = re.findall(findInq,item)         # 添加概述
            if len(inq) != 0:
                inq = inq[0].replace("。","")      # 去掉句号
                data.append(inq)
            else:
                data.append(" ")                   # 留空
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?',' ',bd)     # 去掉<br/>
            db = re.sub('/',' ',bd)      # 替换 /
            data.append(bd.strip())      # 去掉前后的空格
            datalist.append(data)    # 把处理好的一部电影放入datalist
    return datalist

# 等到一个指定URL内容
def askUrl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' \
                      '(KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }   # 用户代理，表示豆瓣服务器，我们是什么机器（浏览器）
    req = urllib.request.Request(url,headers=headers)
    html = ""    # 接收返回的信息
    try:
        responce = urllib.request.urlopen(req)
        html = responce.read().decode('utf-8')

    except:
        pass
    return html

# 保存数据
def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣评分250',cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情连接","图片连接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savepath)     # 保存

def saveData2DB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"'+data[index]+'"'
        sql = '''
            insert into movie250 (
            info_link,pic_link,cname,ename,score,rated,instroduction,info)
            values(%s)'''%",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()



def init_db(dbpath):
    sql = '''
        create table movie250 (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        instroduction text,
        info text
        )
    '''     #创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
    print("爬取完毕！")



