import json
import pymysql
from flask import Flask, request
from flask import jsonify
from pymysql.cursors import DictCursor

app = Flask(__name__)

#数据库初始化
def sql_init():
    conn = pymysql.connect(host='110.40.239.161', user='Cebudongle', passwd='Cebudongle123', port=3306,
                           db='whitepenguin', charset='utf8', autocommit=True)
    cursor = conn.cursor(DictCursor)
    return cursor

#----------资讯获取------------#
@app.route("/news")
# 只接受get方法访问
#@app.route("/", methods=["GET"])
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
    #requestArgs = request.values
    ID = request.args.get("userOpenid",'')
    ID = ID.replace("-","_")
    #get username , password
    if (ID != None):
        conn = pymysql.connect(host='110.40.239.161', user='Cebudongle', passwd='Cebudongle123', port=3306,
                               db='wp_user', charset='utf8', autocommit=True)
        cursor = conn.cursor()
        cursor.execute("create table if not exists "+ ID +" (user_likes_title varchar(80) unique, user_likes_url varchar(200))")
        cursor.execute("ALTER TABLE `wp_user`." + ID +" CHANGE COLUMN `user_likes_title` `user_likes_title` VARCHAR(80) CHARACTER SET 'utf8mb4' NULL DEFAULT NULL")
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
    #cursor.execute("select count(*) from " + ID + " where user_likes_title="+user_likes_title)
    add_user_likes_sql = "Insert ignore into " + ID + " values( '" +  user_likes_title + "', '" + user_likes_url +  "' );"
    cursor.execute(add_user_likes_sql)
    return "ojbk"

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
    cursor.execute("SELECT * FROM "+ ID +" where user_likes_title is not null")
    result = cursor.fetchall()
    print(result)
    return result

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
