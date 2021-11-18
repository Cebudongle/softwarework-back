import time
from datetime import datetime
from urllib.parse import urlencode
import emoji
import pymysql
import pymysql.converters
import requests
from bs4 import BeautifulSoup
from pymysql.converters import escape_string

import requests
import time
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium import webdriver


id = 1
def dataBase_init():
    #conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', port=3306, db='crawler_test1',autocommit=True)
    conn = pymysql.connect(host='123.60.214.55', user='ce', passwd='Cebudongle123', port=3306, db='whitepenguin',autocommit=True)
    cur = conn.cursor()  # 生成游标对象
    createTableSql = "CREATE TABLE IF NOT EXISTS " + "csdn_hotlist " + "(date varchar(10), id varchar(20), blogTitle varchar(80), blogUrl varchar(200), blogBrief varchar(600), blogText longtext);"
    cur.execute(createTableSql)
    iniTableSql = "delete from " + "csdn_hotlist;"
    cur.execute(iniTableSql)

    cur.close()
    conn.commit()
    conn.close()
    return 1

def dataBase_insert(blogTitle, blogUrl, blogBrief, blogText):
    #conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', port=3306, db='crawler_test1',autocommit=True)
    conn = pymysql.connect(host='123.60.214.55', user='ce', passwd='Cebudongle123', port=3306, db='whitepenguin',autocommit=True)
    cur = conn.cursor()  # 生成游标对象
    global id
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    date = str(year) + "/" + str(month) + "/" + str(day)
    id1 = str(id)
    blogText = emoji.demojize(blogText)
    insertTableSql = "insert into " + "`csdn_hotlist` " + "values( '" + date + "', '" + id1 + "', '" + blogTitle + "', '" + blogUrl + "', '" + blogBrief + "', '" + blogText + "' );"
    id += 1
    cur.execute(insertTableSql)
    cur.close()
    conn.commit()
    conn.close()
    return None

def get_list():
    url = "https://blog.csdn.net/rank/list"
    driver = webdriver.Chrome('D:/迅雷下载/chromedriver_win32/chromedriver')
    driver.get(url)
    js = '''
                let height = 0
        let interval = setInterval(() => {
            window.scrollTo({
                top: height,
                behavior: "smooth"
            });
            height += 500
        }, 500);
        setTimeout(() => {
            clearInterval(interval)
        }, 20000);
    '''
    driver.execute_script(js)
    time.sleep(20)
    source = driver.page_source
    # url_list=re.findall('href=\"(.*?)\"',source,re.S)
    # url_list=re.findall('<a target=\"_blank\" href=\"(.*?)\" class=\"title\">(.*?)</a>',source,re.S)
    # url_list=re.findall('href=\"(.*?)\" class=\"title\">(.*?)</a>',source,re.S)
    url_list = re.findall('<a target=\"_blank\" href=\"(.*?)\" class=\"title\">(.*?)</a>', source, re.S)

    cnt = 0
    for ur in url_list:
        name = ur[1]
        link = "\"" + ur[0]
        # print(link.find('\"'),name)
        p = 0
        i = 0
        for ch in link:
            if ch == '\'' or ch == '\"':
                p = i
            i = i + 1
        link = link[p + 1:]
        print("NO.", cnt + 1)
        print("文章名：《" + name + "》")
        print("文章链接：" + link)
        dataBase_insert(name,link,"","")
        # if cnt >= 10 : break
        cnt = cnt + 1

    print("total count = ", cnt)
    driver.close()

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
            get_list()
            # 定时一天爬取一次
            time.sleep(2000)
        else:
            print("Time out, stop.")
            break

if __name__ == "__main__":
    main()