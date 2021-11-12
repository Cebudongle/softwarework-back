
import requests
import time
import urllib
from datetime import datetime
from urllib.parse import urlencode
from bs4 import BeautifulSoup


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
            for list in divs:
                blogUrl = list.get("data-url")
                blogTitle = list.find("div", {"class": "title"}).get("title")
                blogBrief = list.find("p", {"class": "line-clamp"}).string
                blogText = getText(blogUrl)
                #打印爬取信息
                print("文章名：《"+blogTitle+"》")
                print("文章链接：" + blogUrl)
                print("文章简介：" + blogBrief)
                if (blogText!=False):
                    print("文章内容：" + blogText)
                print("\n")
                # 保存爬取信息
                # with open('1.txt', "a+", encoding="UTF-8") as f:
                #     f.write("文章名：《" + blogTitle + "》\n")
                #     f.write("文章链接：" + blogUrl + "\n")
                #     f.write("\n")
                #print(blogTitle + "------记录成功！\n")
                #print(response.content.decode("UTF-8"))
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
    if(t!=None):
        return t.text
    else:
        return False


def main():
    # 定时爬取
    while True:
        # 设置爬取截止时间（可删
        if datetime.now() < datetime(2022, 1, 1, 12, 00, 00):
            print("----------------------------------")
            # 输出当前爬取的时间
            print(datetime.now())

            for number in range(0, 3):  # 3Pages
                getPage(number)
                print("\n")
            # 定时一天爬取一次
            time.sleep(20)
        else:
            print("Time out, stop.")
            break;


if __name__ == "__main__":
    main()

