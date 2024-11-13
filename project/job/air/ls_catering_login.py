import argparse
import json
# import os
from datetime import datetime

import pymysql
import requests

##  http://47.104.223.137:15901/api/v1/ocr_file

def getSession():
    url = 'http://219.146.67.221:23111/dcloud-auth/auth/user/getVcode?vcodeId=75cd1be3-70f7-383b-082c-5aa1a6a2c3c2'
    response = requests.get(url)
    if response.status_code == 200:
        with open('./image/cateringLog.jpg', 'wb') as f:
            f.write(response.content)
        with open('./image/cateringLog.jpg', 'rb') as f:
            files = {'file': f}
            response = requests.post('http://192.168.110.159:8001/api/v1/ocr_file', files=files)
            print(response)
            code = json.loads(response.text)['data']['text'][0]
            print(code)

## 崂山区餐饮油烟在线监测平台-登录
if __name__ == '__main__':
    global start, end
    getSession()