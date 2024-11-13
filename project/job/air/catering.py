import argparse
import json
# import os
from datetime import datetime

import pymysql
import requests

from core.config import base_config_info, air_config_info

# dir_path = os.path.dirname(os.path.abspath(__file__))
# print(dir_path)


# 百度识别账号与密码
# API_KEY = "groaSgDrECGhtXRavZ6yQ04i"
# SECRET_KEY = "FIKPOIGxEYGD7lhEInqMGtdqc1CqgR4G"


# 获取百度识别的access_token
# def get_access_token():
#     """
#     使用 AK，SK 生成鉴权签名（Access Token）
#     :return: access_token，或是None(如果错误)
#     """
#     url = "https://aip.baidubce.com/oauth/2.0/token"
#     params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
#     return str(requests.post(url, params=params).json().get("access_token"))


# def get_file_content_as_base64(path, urlencoded=False):
#     """
#     获取文件base64编码
#     :param path: 文件路径
#     :param urlencoded: 是否对结果进行urlencoded
#     :return: base64编码信息
#     """
#     with open(path, "rb") as f:
#         content = base64.b64encode(f.read()).decode("utf8")
#         if urlencoded:
#             content = urllib.parse.quote_plus(content)
#     return content


def getSession():
    url = 'http://221.215.122.210:8102/api/verify?random'
    response = requests.get(url)
    if response.status_code == 200:
        with open('qr_code.jpg', 'wb') as f:
            f.write(response.content)
        with open('qr_code.jpg', 'rb') as f:
            files = {'file': f}
            response = requests.post('http://192.168.110.159:8001/api/v1/ocr_file', files=files)
            print(response)
            code = json.loads(response.text)['data']['text'][0]
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://221.215.122.210:8088',
        'Referer': 'http://221.215.122.210:8088/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'token': 'null',
    }

    json_data = {
        'username': 'qdhl',
        'password': 'a02d589cd5240ba12cc6862bf668610a',
        'vcode': code,
    }

    response = requests.post('http://221.215.122.210:8102/api/login/', headers=headers, json=json_data, verify=False)
    print(response.json()['data']['token'])
    return response.json()['data']['token']


def getEnterprise(type_list):
    conn1 = pymysql.connect(**base_config_info)
    cursorTarget1 = conn1.cursor()
    for i in type_list:
        # print('regionId')
        # print('regionName')
        query1 = "SELECT * FROM t_pub_company WHERE CREDIT_NO = %s"
        cursorTarget1.execute(query1, [i['enterpriseId']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchall()
        if len(results1) == 0:
            sql1 = '''insert into t_pub_company (
                                                            CREDIT_NO,
                                                            CREDIT_NO_TRUE,
                                                            COMPANY_NAME,
                                                            DISTRICT_CODE,
                                                            SYS_CITY_CODE,
                                                            SYS_COUNTY_CODE
                                                            ) values(%s,%s,%s,%s,'370200000000','370212000000')'''
            insert = cursorTarget1.execute(sql1, [i['enterpriseId'],
                                                  i['enterpriseId'],
                                                  i['enterpriseName'],
                                                  i['regionName']
                                                  ])
    conn1.commit()
    cursorTarget1.close()
    # 关闭连接
    conn1.close()


def getData():
    print('执行')
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'http://221.215.122.210:8088',
        'Referer': 'http://221.215.122.210:8088/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'token': getSession()
    }
    params = {
        'index': '1',
        'size': '50',
        'enterpriseName': '',
        'pointName': '',
        'mn': '',
        'overproof': '',
    }

    response = requests.get('http://221.215.122.210:8102/api/monitor/data/pointList', params=params, headers=headers,
                            verify=False)
    type_list = response.json()["data"]["records"]
    print(type_list)
    print(type_list)
    # getEnterprise(type_list)
    conn = pymysql.connect(**air_config_info)
    cursorTarget = conn.cursor()
    for i in type_list:
        query = "SELECT * FROM t_air_catering_hour WHERE CREDIT_NO = %s and MONITOR_TIME = %s and POINT_NAME = %s"
        cursorTarget.execute(query, [i['enterpriseId'], i['lastDt'], i['pointName']])
        # 获取所有记录列表
        results = cursorTarget.fetchall()
        if len(results) == 0:
            sql = '''insert into t_air_catering_hour (
                                                       CREDIT_NO,
                                                       COMPANY_NAME,
                                                       POINT_NAME,
                                                       MN_CODE,
                                                       A34041,
                                                       A01002,
                                                       A01001,
                                                       ON_LINE,
                                                       POINT_ID,
                                                       MONITOR_TIME,
                                                       SYS_CITY_CODE,
                                                       SYS_COUNTY_CODE
                                                       ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
            insert = cursorTarget.execute(sql, [i['enterpriseId'],
                                                i['enterpriseName'],
                                                i['pointName'],
                                                i['mn'],
                                                i['a34041'],
                                                i['a01002'],
                                                i['a01001'],
                                                i['onLine'],
                                                i['pointId'],
                                                i['lastDt']
                                                ])
    conn.commit()
    cursorTarget.close()
    # 关闭连接
    conn.close()


def getEnterpriseCode(param):
    conn1 = pymysql.connect(**base_config_info)
    cursorTarget1 = conn1.cursor()
    query1 = "SELECT * FROM t_pub_company WHERE COMPANY_NAME = %s"
    cursorTarget1.execute(query1, param)
    # 获取所有记录列表
    results1 = cursorTarget1.fetchall()
    return results1[0][2]


def getWarn():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'http://221.215.122.210:8088',
        'Referer': 'http://221.215.122.210:8088/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'token': getSession()
    }
    # 获取当前日期
    current_date = datetime.now()

    # 格式化为字符串
    formatted_date = current_date.strftime("%Y-%m-%d")
    params = {
        'mn': '',
        'enterpriseName': '',
        'regionId': '',
        'beginTime': '2023-02-01 00:00:00',
        'endTime': formatted_date + ' 00:00:00',
        'index': '1',
        'size': '1000',
    }

    response = requests.get('http://221.215.122.210:8102/api/monitor/warnData/', params=params, headers=headers,
                            verify=False)
    type_list = response.json()["data"]["list"]
    for i in type_list:
        # 创建一个游标对象
        conn = pymysql.connect(**base_config_info)
        cursor = conn.cursor()
        # 获取企业统一信用码
        code = getEnterpriseCode(i['enterpriseName'])
        name = i['enterpriseName']
        type = 4
        stationCode = i['mn']
        stationName = i['enterpriseName']
        time = i['dataTime']
        warnType = 1
        monitorData = i['a34041']
        status = 1
        warnMode = 1
        warnDetails = '浓度的小时最大值浓度为：' + i['a34041'] + '，阈值为：1,超标' + i['a34041'] + '倍'
        warnFactor = '浓度'
        cityCode = '370200000000'
        countyCode = '370212000000'
        # 插入数据，如果已存在则跳过
        user_data = (
            code, name, type, stationCode, stationName, time, warnType, warnDetails, status, monitorData, warnMode,
            warnFactor, cityCode, countyCode)

        try:
            cursor.execute('''
                       INSERT INTO t_air_warn (BUSINESS_CODE,
                        BUSINESS_NAME,
                        BUSINESS_TYPE,
                        STATION_CODE,
                        STATION_NAME,
                        MONITOR_TIME,
                        WARN_TYPE,
                        WARN_DETAILS,
                        STATUS,
                        MONITOR_DATA,
                        WARN_MODE,
                        WARN_FACTOR,
                        SYS_CITY_CODE,
                        SYS_COUNTY_CODE) VALUES 
                       (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                       ON DUPLICATE KEY UPDATE SYS_UPDATE_TIME = now()
                   ''', user_data)
        except pymysql.IntegrityError as e:
            if e.args[0] == 1062:  # 1062表示唯一键冲突
                print("User already exists. Skipping insertion.")
            else:
                raise
        # 提交更改
        conn.commit()
        # 关闭连接
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='解析参数')
    parser.add_argument('--dateType', '-d', help='时间类型(1=小时；2=天；3=月；4=年)')
    args = parser.parse_args()
    if int(args.dateType) == 1:
        getData()
    elif int(args.dateType) == 2:
        getWarn()

    
