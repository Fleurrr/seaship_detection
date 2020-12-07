# -*- coding: utf-8 -*-
# @Time : 2020-12-05 18:25
# @Author : sloan
# @Email : 630298149@qq.com
# @File : flask_client.py
# @Software: PyCharm
# ! -*- coding:utf-8 -*-

import json
import time
import requests
import base64

url = 'http://127.0.0.1:4392/api/detect'
img_path = 'test.jpg'
with open(img_path, "rb") as f:
    base64_str = base64.b64encode(f.read()).decode('utf-8')
print(type(base64_str))
data = {"image":base64_str,"roi":''}
print(data)
#POST 请求
response = requests.post(url,data)
#返回结果
print(response)
answer = response.json()
print('predict results',answer,type(answer))