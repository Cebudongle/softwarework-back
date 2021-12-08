import json
import pymysql
from flask import Flask, request
from flask import jsonify
from pymysql.cursors import DictCursor
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

#数据库初始化
def sql_init():
    conn = pymysql.connect(host='110.40.239.161', user='Cebudongle', passwd='Cebudongle123', port=3306,
                           db='whitepenguin', charset='utf8', autocommit=True)
    cursor = conn.cursor(DictCursor)
    return cursor

#----------资讯获取------------#
@app.route("/news", methods=["GET"])
# 只接受get方法访问
def check_news():
    # 默认返回内容
    return_dict = {'code': 1, 'result': False, 'msg': '请求成功'}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '504'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_data = request.args.to_dict()
    # 对参数进行操作
    return_dict['result'] = sql_result_news()
    print(return_dict)
    return json.dumps(return_dict, ensure_ascii=False)
# 功能函数
def sql_result_news():
    cursor = sql_init()
    cursor.execute("SELECT * FROM osChina WHERE id is not NULL")
    result = cursor.fetchall()
    #conn.close()
    return result

#----------热榜获取------------#
@app.route("/hotlist")
def check_hotlist():
    # 默认返回内容
    return_dict = {'code': 1, 'result': False, 'msg': '请求成功'}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '504'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_data = request.args.to_dict()
    # 对参数进行操作
    return_dict['result'] = sql_result_hotlist()
    return json.dumps(return_dict, ensure_ascii=False)

def sql_result_hotlist():
    cursor = sql_init()
    cursor.execute("SELECT * FROM csdn_hotlist WHERE id is not NULL")
    result = cursor.fetchall()
    return result

#----------用户信息-----------#
# --------返回openID----------#
@app.route("/login", methods=["GET"])
def login():
    ID = request.args.get("userOpenid",'')
    ID = ID.replace("-","_")
    if (ID != None):
        conn = pymysql.connect(host='110.40.239.161', user='Cebudongle', passwd='Cebudongle123', port=3306,
                               db='wp_user', charset='utf8', autocommit=True)
        cursor = conn.cursor()
        cursor.execute("Insert ignore into `wp_user`.`wp_user` values( '" + ID +"')")
        conn.close()
    return ID

#----------加入收藏-----------#
#-—---返回 openID+文章名+url---#
@app.route("/add_user_likes")
def add_user_likes():
    ID = request.args.get("userOpenid", '')
    ID = ID.replace("-", "_")
    user_likes_title = request.args.get("title", '')
    user_likes_url = request.args.get("url", '')
    print(user_likes_title)
    print(user_likes_url)
    conn = pymysql.connect(host='110.40.239.161', user='Cebudongle', passwd='Cebudongle123', port=3306,
                           db='wp_user', charset='utf8', autocommit=True)
    cursor = conn.cursor(DictCursor)
    add_user_likes_sql = "Insert ignore into wp_user_likes   values( '" + ID + "', '" + user_likes_title + "', '" + user_likes_url +  "' );"
    cursor.execute(add_user_likes_sql)
    return "add user_like successfully"

#----------删除收藏-----------#
#-—---返回 openID+文章名+url---#
@app.route("/del_user_likes")
def del_user_likes():
    ID = request.args.get("userOpenid", '')
    ID = ID.replace("-", "_")
    user_likes_title = request.args.get("title", '')
    print(user_likes_title)
    conn = pymysql.connect(host='110.40.239.161', user='Cebudongle', passwd='Cebudongle123', port=3306,
                           db='wp_user', charset='utf8', autocommit=True)
    cursor = conn.cursor(DictCursor)
    del_user_likes_sql = "Delete from wp_user_likes where user_ID = '" + ID + "' and user_likes_title = '" + user_likes_title  + "';"
    cursor.execute(del_user_likes_sql)
    return "delete user_like successfully"

#----------查看收藏-----------#
# --------返回openID----------#
@app.route("/get_user_likes")
def check_user_likes():
    # 默认返回内容
    return_dict = {'code': 1, 'result': False, 'msg': '请求成功'}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '504'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

    return_dict['result'] = sql_result_user_likes()
    return json.dumps(return_dict, ensure_ascii=False)

def sql_result_user_likes():
    ID = request.args.get("userOpenid", '')
    ID = ID.replace("-", "_")
    print(ID)
    conn = pymysql.connect(host='110.40.239.161', user='Cebudongle', passwd='Cebudongle123', port=3306,
                           db='wp_user', charset='utf8', autocommit=True)
    cursor = conn.cursor(DictCursor)
    cursor.execute("SELECT * FROM wp_user_likes where user_ID = '" + ID + "';")
    result = cursor.fetchall()
    print(result)
    return result

#---------查看收藏具体---------#
# --------返回 url------------#
@app.route("/user_likes_details")
def check_user_likes_details():
    # 默认返回内容
    return_dict = {'code': 1, 'result': False, 'msg': '请求成功'}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '504'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    return_dict['result'] = user_likes_details()
    return json.dumps(return_dict, ensure_ascii=False)

def user_likes_details():
    user_likes_url = request.args.get("url", '')
    print(user_likes_url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/73.0.3683.86 Safari/537.36",
    }
    params = {
        "classification": "5593654",
        "type": "ajax",
    }
    res = requests.get(user_likes_url, headers=headers, params=params)
    soup = BeautifulSoup(res.content.decode("UTF-8"), "html.parser")
    # osChina
    t = soup.find("div", {"class": "article-detail"})
    if (t != None):
        if (t.text!=""):
            print(t.text)
            return t.text
    else:
        t1 = soup.find("div", {"id": "content_views"})
        if (t1!=None):
            if (t1.text!=""):
                print(t1.text)
                return t1.text
    if(t1.text!="" and t.text!=""):
        return user_likes_url


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
