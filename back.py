# Python 
# 2021/11/29 20:01
import os
from flask import Flask, request
import requests

app = Flask(__name__)


# 测试
@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/search/github')
def search_github():
    keyword = request.values.get('q')
    print("github search q: ", keyword)

    response = requests.get(
        'https://api.github.com/search/repositories',
        params={'q': keyword},
    )
    print("github search result status_code: ", response.status_code)
    json_response = response.json()
    return json_response


@app.route('/search/gitee')
def search_gitee():
    keyword = request.values.get('q')
    print("gitee search q: ", keyword)

    response = requests.get(
        'https://gitee.com/api/v5/search/repositories',
        params={'q': keyword},
    )
    print("gitee search result status_code: ", response.status_code)
    json_response = response.json()
    json_response = {'items': json_response}
    return json_response


if __name__ == '__main__':
    app.run(debug=False)
