#-- coding:UTF-8 --
import time
import argparse

from sqlalchemy.orm import Session
from database.mysql import get_air_db
from util import h
from job.pse import ls_login
import requests
import json
from mod.slagcar import TAirSlagcarViolationRecord
from core import logger
from datetime import datetime, timedelta

h._init()

## 监测数据
def getBean(bean, recordBean, detailsBean, carBean):
    recordBean['snapshot_time'] = datetime.strptime(recordBean['snapshot_time'],"%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d %H:%M:%S')
    recordBean['violation_time'] = datetime.strptime(recordBean['violation_time'],"%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d %H:%M:%S')
    # 车辆类型
    if recordBean['car_type'] == '大型车' :
        recordBean['car_type'] = 1
    if recordBean['car_type'] == '小型车':
        recordBean['car_type'] = 2
    if recordBean['car_type'] == '渣土车':
        recordBean['car_type'] = 3
    if recordBean['car_type'] == '疑似渣土车':
        recordBean['car_type'] = 4
    if recordBean['car_type'] == '其他':
        recordBean['car_type'] = 5
    return bean(
             POINT_NAME = recordBean['monitor'],
             CAR_NO = recordBean['car_num'],
             IS_RECORD = recordBean['is_local_ztc'],
             CAR_TYPE = recordBean['car_type'],
             CAPTURE_TIME = recordBean['snapshot_time'],
             ORG_NAME = carBean['company'],
             CAR_HEAD_NO = '',
             LINKMAN = carBean['contacts'],
             REGION_NAME = carBean['region'],
             AUDIT_TIME = recordBean['violation_time'],
             VIOLATION_TYPE_CODE = recordBean['vio_type_ids'],
             VIOLATION_TYPE_NAME = recordBean['violation_type'],
             VIOLATION_LEVEL = recordBean['viol_degree'],
             MARK_STATUS = detailsBean['status'],
             LANE_NUMBER=detailsBean['lane_number'],
             ELAPSED_TIME =  recordBean['snapshot_time'],
             CAR_HEAD_PICTURE_PATH = detailsBean['pic_path'],

             SYS_CITY_CODE="370200000000",
             SYS_COUNTY_CODE="370212000000",
    )

headers_init = h.buildHeader_ls_slagcar_init()
def getToken():
    params = {
        'appId': '29',
        'serverName': 'ztc-snapshot.qdztc.czczh.cn',
        'username': 'qdlsq',
    }
    response = requests.get('https://uuc.it.czczh.cn/gw/novauc/anonymous/getClient', params=params, headers=headers_init)
    print('获取token-getClient：' + response.text)
    resp = json.loads(response.text)
    files = {
        'username': (None, 'qdlsq'),
        'password': (None, '123456'),
        'grant_type': (None, 'password'),
        'client_id': (None, resp['data']['clientId']),
        'client_secret': (None, resp['data']['clientSecretStr']),
        'remember': (None, 'true')
        # 'local_time': (None, '1729661730.258'),
    }

    response = requests.post('https://uuc.it.czczh.cn/gw/novauc/oauth/token', headers=headers_init, files=files)
    resp = json.loads(response.text)
    print('获取token：' + resp['access_token'])
    return resp['access_token']

accessToken = getToken()
headers = h.buildHeader_ls_slagcar(accessToken)
print('headers：' + str(headers))

cookies = h.buildCookies_ls_slagcar()

def getSlagcarRecordList(startTime, endTime):
    url = 'https://ztc-snapshot.qdztc.czczh.cn/api/violation_manage/violation_snap/get-data-list?project_id=1209&page=1&page_size=40&snap_start_time='+startTime+'&snap_end_time='+endTime
    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
    )
    print('列表：'+response.text)
    return response
def getRecordDetails(violationId):
    params = {
        'project_id': '1209',
        'snapshot_id': violationId,
        'is_imp': 'false',
        'is_box': 'false',
    }

    response = requests.get(
        'https://ztc-snapshot.qdztc.czczh.cn/api/snapshot_manage/snapshot/get-snapshot-data',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print('详情基本信息：'+response.text)
    return response

def getRecordCarInfo(carNo):
    params = {
        'project_id': '1209',
        'car_no': carNo,
    }

    response = requests.get(
        'https://ztc-snapshot.qdztc.czczh.cn/api/snapshot_manage/car_info/get_local_car_info',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    print('详情车辆信息：'+response.text)
    return response
def mainSpider(startTime, endTime):
    global bean, datetimeTemp
    logger.success("渣土车违规记录采集启动成功")

    headers = h.buildHeader_ls()
    air_db: Session = next(get_air_db())

    # 获取违规记录列表
    response = getSlagcarRecordList(startTime, endTime)
    # 处理异常
    try:
        resp = json.loads(response.text)
    except:
        mainSpider(startTime, endTime)
    print('列表数量：' +str(len(resp["data"])))
    # 循环列表
    for r in range(len(resp["data"])):
        reRecordBean = resp["data"][r]
        print('列表第'+str(r) +'条数据：'+ str(reRecordBean))

        # 获取详情-基本信息
        response2 = getRecordDetails(reRecordBean['violation_id'])
        # 获取详情-车辆信息
        response3 = getRecordCarInfo(reRecordBean['car_num'])
        # 处理异常
        try:
            resp2 = json.loads(response2.text)
            reRecordDetailsBean = resp2["data"]
        except:
            reRecordDetailsBean['status'] = None
            reRecordDetailsBean['lane_number'] = ''
            reRecordDetailsBean['pic_path'] = ''
            # continue
        try:
            resp3 = json.loads(response3.text)
            reRecordCarBean = resp3["data"]
        except:
            reRecordCarBean['company'] = ''
            reRecordCarBean['contacts'] = ''
            reRecordCarBean['region'] = ''
            # continue

        bean = TAirSlagcarViolationRecord.TAirSlagcarViolationRecord
        table = getBean(bean, reRecordBean, reRecordDetailsBean, reRecordCarBean)

        air_db.query(bean).filter(
                                  bean.POINT_NAME == reRecordBean['monitor'],
                                  bean.CAR_NO == reRecordBean['car_num'],
                                  bean.CAPTURE_TIME == reRecordBean['snapshot_time']).delete()
        air_db.add(table)
    air_db.commit()
    air_db.close()


## 渣土车智能抓拍系统-》违规管理-》违规记录
if __name__ == '__main__':
    global start, end

    current_date = datetime.now()
    two_hours_ago = current_date - timedelta(days=2000)
    startTime = two_hours_ago.strftime("%Y-%m-%d+%H:00:00")
    endTime = current_date.strftime("%Y-%m-%d+%H:00:00")

    logger.success('采集日期：'+startTime+'到'+endTime)
    logger.success("渣土车采集开始...")
    mainSpider(startTime, endTime)
    logger.success("渣土车采集结束!")


