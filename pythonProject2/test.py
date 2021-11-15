import requests
import re
from lxml import etree
import os
import time
import flask



def get_html():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    # 小说目录URL，改变这个URL就可以下载对应的小说
    url = 'http://www.xbiquge.la/6/6818/'
    html = requests.get(url, headers=headers).content.decode('utf-8')
    return html


def get_novel_url(html):
    ''' 获取章节名和链接 '''
    pat2 = r"<dd><a href='(.*?)' >(.*?)</a></dd>"
    title_name = re.findall(pat2, html)
    # 小说保存文件名称
    path = '真武世界'
    if not os.path.exists(path):
        os.makedirs(path)
    for title in title_name:
        # 章节URL
        novel_url = title[0]
        # 章节名
        novel_name = title[1]
        # 构造章节URL
        newUrl = 'http://www.xbiquge.la' + novel_url

        response = requests.get(newUrl).content.decode('utf-8', 'ignore')
        response = etree.HTML(response)
        # 获取章节内容
        content = response.xpath('//*[@id="content"]/text()')
        # content = content[0].replace('?', '')

        try:
            # 下载小说
            print("正在下载小说----->>>>>> %s" % novel_name)
            filename = path + '/' + '{}.txt'.format(novel_name)
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(content)
                time.sleep(1)
        except Exception as e:
            print("下载出错!", e)


def main():
    html = get_html()
    get_novel_url(html)


if __name__ == '__main__':
    main()