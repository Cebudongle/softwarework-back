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


@app.route('/search')
def search():
    keyword = request.values.get('q')
    per_page = request.values.get('per_page')
    page = request.values.get('page')

    print("search q: ", keyword, "per_page: ", per_page, "page: ", page)

    response1 = requests.get(
        'https://api.github.com/search/repositories',
        params={'q': keyword,
                'per_page': per_page,
                'page': page
                },
    )
    print("github search result status_code: ", response1.status_code)
    json_response1 = response1.json()

    response2 = requests.get(
        'https://gitee.com/api/v5/search/repositories',
        params={'q': keyword,
                'per_page': per_page,
                'page': page
                },
    )
    print("gitee search result status_code: ", response2.status_code)
    json_response2 = response2.json()

    json_response={'items1': json_response1['items'], 'items2': json_response2}

    return json_response


@app.route('/search/github')
def search_github():
    keyword = request.values.get('q')
    per_page = request.values.get('per_page')
    page = request.values.get('page')

    print("github search q: ", keyword, "per_page: ", per_page, "page: ", page)

    response = requests.get(
        'https://api.github.com/search/repositories',
        params={'q': keyword,
                'per_page': per_page,
                'page': page
                },
    )
    print("github search result status_code: ", response.status_code)
    json_response = response.json()
    return json_response


@app.route('/search/gitee')
def search_gitee():
    keyword = request.values.get('q')
    per_page = request.values.get('per_page')
    page = request.values.get('page')

    print("gitee search q: ", keyword, "per_page: ", per_page, "page: ", page)

    response = requests.get(
        'https://gitee.com/api/v5/search/repositories',
        params={'q': keyword,
                'per_page': per_page,
                'page': page
                },
    )
    print("gitee search result status_code: ", response.status_code)
    json_response = response.json()
    json_response = {'items': json_response}
    return json_response


if __name__ == '__main__':
    app.run()
