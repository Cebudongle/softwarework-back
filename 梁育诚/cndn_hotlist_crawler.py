import requests
import time
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium import webdriver


url="https://blog.csdn.net/rank/list"
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
url_list=re.findall('<a target=\"_blank\" href=\"(.*?)\" class=\"title\">(.*?)</a>',source,re.S)

cnt=0
for ur in url_list:
    name=ur[1]
    link="\""+ur[0]
    # print(link.find('\"'),name)
    p=0
    i = 0
    for ch in link:
        if ch == '\'' or ch == '\"':
            p=i
        i = i + 1
    link=link[p+1:]
    print("NO.",cnt+1)
    print("文章名：《" + name + "》")
    print("文章链接：" + link)

    with open('csdnhotlist.txt', "a+", encoding="UTF-8") as f:
        # f.write("NO.",cnt+1,"\n")
        f.write("文章名：《" + name + "》\n")
        f.write("文章链接：" + link + "\n")
        f.write("\n")
        print(name + "------记录成功！\n")

    # if cnt >= 10 : break
    cnt = cnt + 1

print("total count = ",cnt)
driver.close()
