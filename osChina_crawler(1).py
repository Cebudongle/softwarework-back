import time
from datetime import datetime
from urllib.parse import urlencode
import emoji

import pymysql
import pymysql.converters
import requests
from bs4 import BeautifulSoup

id = 1
def dataBase_init():
    #conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', port=3306, db='crawler_test1',autocommit=True)
    #conn = pymysql.connect(host='123.60.214.55', user='ce', passwd='Cebudongle123', port=3306, db='whitepenguin',autocommit=True)
    conn = pymysql.connect(host='110.40.239.161', user='Cebudongle', passwd='Cebudongle123', port=3306, db='whitepenguin',charset='utf8',autocommit=True)
    cur = conn.cursor()  # 生成游标对象
    #createTableSql = "CREATE TABLE IF NOT EXISTS " + "osChina " + "(date varchar(10), id varchar(20), blogTitle varchar(80), blogUrl varchar(200), blogBrief varchar(600), blogText longtext);"
    createTableSql = "CREATE TABLE IF NOT EXISTS " + "osChina " + "(date varchar(10), id varchar(20), blogTitle varchar(80), blogUrl varchar(200), blogBrief varchar(600));"
    cur.execute(createTableSql)
    iniTableSql = "delete from " + "osChina;"
    cur.execute(iniTableSql)

    cur.close()
    conn.commit()
    conn.close()
    return 1

def dataBase_insert(blogTitle, blogUrl, blogBrief, blogText):
    #conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', port=3306, db='crawler_test1',autocommit=True)
    #conn = pymysql.connect(host='123.60.214.55', user='ce', passwd='Cebudongle123', port=3306, db='whitepenguin',autocommit=True)
    conn = pymysql.connect(host='110.40.239.161', user='Cebudongle', passwd='Cebudongle123', port=3306,db='whitepenguin', charset='utf8', autocommit=True)
    cur = conn.cursor()  # 生成游标对象
    global id
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    date = str(year) + "/" + str(month) + "/" + str(day)
    id1 = str(id)
    insertTableSql = "insert into " + "`osChina` " + "values( '" + date + "', '" + id1 + "', '" + blogTitle + "', '" + blogUrl + "', '" + blogBrief +  "', '" + blogText + "' );"
    id += 1
    cur.execute(insertTableSql)
    cur.close()
    conn.commit()
    conn.close()
    return None

def getPage(number):
    #访问头部
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/73.0.3683.86 Safari/537.36",
    }
    params = {
        "classification": "5593654",
        "p": str(number),
        "type": "ajax",
    }
    #爬取开源中国综合资讯页面
    url = "https://www.oschina.net/news/industry" + urlencode(params)

    try:
        response = requests.get(url,headers=headers,params=params)
        if response.status_code == 200: #正常连接
            soup = BeautifulSoup(response.content.decode("UTF-8"), "html.parser")
            #查找 <div class = "item news-item news-item-hover"标签下内容 ，并存入divs
            divs = soup.find_all('div', {"class" : "item news-item news-item-hover"})
            global id
            for list in divs:
                if(list.get("data-url")!=''):
                    blogUrl = list.get("data-url")
                else:
                    continue
                blogTitle = list.find("div", {"class": "title"}).get("title")
                blogBrief = list.find("p", {"class": "line-clamp"}).text
                blogBrief = blogBrief.replace("'","''")
                blogBrief = emoji.demojize(blogBrief)
                blogText = getText(blogUrl)
                if(type(blogText)!=bool):
                    blogText = blogText.replace("'", "''")
                    blogText = emoji.demojize(blogText)
                #打印爬取信息
                print("文章名：《"+blogTitle+"》")
                print("文章链接：" + blogUrl)
                print("文章简介：" + blogBrief)
                print("\n")
                #文章内容爬取
                if (blogText!=False):
                    print("文章内容：" + blogText)
                print("\n")
                if (type(blogText)!=str):
                    blogText = ""
                dataBase_insert(blogTitle,blogUrl,blogBrief,blogText)
                #dataBase_insert(blogTitle,blogUrl,blogBrief)
    except requests.ConnectionError:
        return None

#获取单个链接内的文章内容
def getText(url):
    #申请头部
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/73.0.3683.86 Safari/537.36",
    }
    params = {
        "classification": "5593654",
        "type": "ajax",
    }
    res = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(res.content.decode("UTF-8"), "html.parser")
    #返回指定标签下的文章内容
    t = soup.find("div", {"class": "article-detail"})
    #img = soup.find("img").get("src")
    if(t!=None):
        return t.text
    else:
        return False


def main():
    # 定时爬取
    while True:
        # 设置爬取截止时间2022/1/1 12:00:00（可删
        if datetime.now() < datetime(2022, 1, 1, 12, 00, 00):
            print("----------------------------------")
            # 输出当前爬取的时间
            print(datetime.now())
            #初始化数据库
            if (dataBase_init()==1):
                print("dataBase initialize succeed!")
            else:
                print("dataBase initialize error.")

            for number in range(0, 4):  # 4Pages
                getPage(number)
                print("\n")
            # 定时5h爬取一次
            time.sleep(18000)
        else:
            print("Time out, stop.")
            break

if __name__ == "__main__":
    main()