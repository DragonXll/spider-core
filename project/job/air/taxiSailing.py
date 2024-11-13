import argparse
import requests
import json

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database.mysql import get_air_db
from mod import TNavigationMonitoringTaxi


def getDataBean(bean, r):
    return bean(MONITOR_TIME=startTime,
                TYPE =3,
                REGION_NAME=r['region_name'],
                ROAD_NO = r['id'],
                SECTION_NAME=r['name'],
                STARTING_POINT=r['start'],
                END_POINT=r['end'],
                PM2_5=r['pm25'],
                PM10=r['pm10'],
                # TSP=r[''],
                # DUST_SOURCE=r[''],
                SYS_STREET_NAME=r['street'],
             SYS_CITY_CODE="370200000000",
             SYS_COUNTY_CODE="370212000000",
    )

def login_getToken():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryoNdyT2IpdytI29HI',
        'Origin': 'https://qingdao.czczh.cn',
        'Referer': 'https://qingdao.czczh.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    data = '------WebKitFormBoundaryoNdyT2IpdytI29HI\r\nContent-Disposition: form-data; name="username"\r\n\r\nqdsczc\r\n------WebKitFormBoundaryoNdyT2IpdytI29HI\r\nContent-Disposition: form-data; name="password"\r\n\r\n468132\r\n------WebKitFormBoundaryoNdyT2IpdytI29HI\r\nContent-Disposition: form-data; name="grant_type"\r\n\r\npassword\r\n------WebKitFormBoundaryoNdyT2IpdytI29HI\r\nContent-Disposition: form-data; name="client_id"\r\n\r\nd70930b3-0654-451a-b2a4-e371e0b96e20\r\n------WebKitFormBoundaryoNdyT2IpdytI29HI\r\nContent-Disposition: form-data; name="client_secret"\r\n\r\n0047af94-13bd-43f9-bd08-b94e1537cd87\r\n------WebKitFormBoundaryoNdyT2IpdytI29HI\r\nContent-Disposition: form-data; name="remember"\r\n\r\ntrue\r\n------WebKitFormBoundaryoNdyT2IpdytI29HI\r\nContent-Disposition: form-data; name="local_time"\r\n\r\n1703669839.809\r\n------WebKitFormBoundaryoNdyT2IpdytI29HI--\r\n'

    response = requests.post('https://uuc.it.czczh.cn/gw/novauc/oauth/token', headers=headers, data=data)
    print('response：', response.text)
    try:
        resp = json.loads(response.text)
    except:
        login_getToken.inits()
    return resp["access_token"];

def getSpiderData(accessToken,startTime):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://qingdao.czczh.cn/pc/main/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'token': accessToken,
    }

    response = requests.get(
        'https://qingdao.czczh.cn/api/car_api_py/car_route_api_v2/get_summary_route_color2_v2?group_id=1&filter_size=30D&month=%E6%97%A5%E5%8F%A0%E5%8A%A0:'+startTime+'%2009:00:00:ALLPOINT&color_map_id=1&check_type=Check',
        headers=headers,
    )
    resp = json.loads(response.text)
    return resp

def spider(startTime):
    air_db: Session = next(get_air_db())
    # login_GetClient()
    accessToken = login_getToken()
    print('access_token：',  accessToken)
    resp = getSpiderData(accessToken,startTime)
    print('response：', len(resp))

    for i in range(0,len(resp)):
        r = resp[i]
        print('r：', r)
        bean = TNavigationMonitoringTaxi
        table = getDataBean(bean,r)

        air_db.query(bean).filter(bean.MONITOR_TIME == startTime,
                                  bean.TYPE == 3,
                                  bean.ROAD_NO == r['id'],
                                  bean.REGION_NAME == r['region_name']
                        ).delete()
        air_db.add(table)
        air_db.commit()
        air_db.close()

## 出租车走航-路段信息【青岛走航大气监测管理系统-》道路统计】
if __name__ == '__main__':
    global bean, startTime
    parser = argparse.ArgumentParser(description='解析参数')
    parser.add_argument('--dayNum', '-dn', help='采集dayNum天数据')
    args = parser.parse_args()
    if(args.dayNum==None):
        dayNum = 1
    else:
        dayNum = int(args.dayNum)
    print('dayNum：', dayNum)

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    for i in range(-dayNum,0):
        print('i：', i)
        # global start, end
        yesterday = current_date + timedelta(days=i)
        startTime = yesterday.strftime("%Y-%m-%d")
        print('startTime：', startTime)

        spider(startTime)

