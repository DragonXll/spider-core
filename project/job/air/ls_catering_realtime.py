#-- coding:UTF-8 --
import time
import argparse

from sqlalchemy.orm import Session
from database.mysql import get_air_db
from util import h
import requests
import json
from mod.catering import TAirCateringRealtime
from core import logger

h._init()

## 监测数据
def getBean(baseBean, dataBean):
    return baseBean(
        CREDIT_NO = '',    #'统一社会信用代码'
        COMPANY_NAME = dataBean['enterShort'], #监控点名称（餐厅名称）
        STATION_ID = dataBean['stationId'],#排口ID
        STATION_NAME = dataBean['stationName'],#排口名称
        MONITOR_TIME = dataBean['dateTime'],#监测时间
        DETECTION_STATUS = dataBean['stationState'], #检测状态（0：正常 1：超标 2：离线  3：冻结）
        LINKAGE_RATIO = dataBean['RUN_RATE'], #联动比
        PURIFIER_STATUS = dataBean['stateGa41'], #净化器状态（0=不在线；1=在线）
        FAN_STATUS = dataBean['stateGa38'], #风机状态（0=不在线；1=在线）
        A34041 = dataBean['RTD_ga23'],#油烟浓度（A34041）
        A01002 = dataBean['RTD_ga24'],#颗粒物（A01002）
        A01001 = dataBean['RTD_ga25'],#非甲烷总烃（A01001）

        SYS_CITY_CODE="370200000000",
        SYS_COUNTY_CODE="370212000000",
    )

cookies= h.buildCookies_ls_catering()
headers = h.buildHeader_ls_catering()
def getPointInfo():
    json_data = {
        'limit': 999,
        'page': 1,
        'areaId': '',
        'enterSize': '',
        'cookingStyle': '',
        'enterId': '',
        'regionCode': '370212',
        'userId': '0d2dccf2965f48fdb22f1951c6903c8b',
        'enterType': '',
        'stationState': '',
        'enterName': '',
        'dataType': '1',
        'dataTime': 'DATA_TIME',
        'stationStateRow': '',
        'factorRow': '',
        'sortBy': 'desc',
        'nationalStateCode': '',
        'nationalRangeCode': '',
        'factor': [
            {
                'mStand': 1,
                'factorCode': 'ga23',
                'uploadCode': 'RTD_ga23',
                'sStand': 1,
                'dataType': 1,
                'factorType': 1,
                'lStand': 1,
                'measureUnit': 'mg/m³',
                'SORTING': 1,
                'uploadName': '油烟浓度',
            },
            {
                'mStand': 5,
                'factorCode': 'ga24',
                'uploadCode': 'RTD_ga24',
                'sStand': 5,
                'dataType': 1,
                'factorType': 1,
                'lStand': 5,
                'measureUnit': 'mg/m³',
                'SORTING': 2,
                'uploadName': '颗粒物浓度',
            },
            {
                'mStand': 10,
                'factorCode': 'ga25',
                'uploadCode': 'RTD_ga25',
                'sStand': 10,
                'dataType': 1,
                'factorType': 1,
                'lStand': 10,
                'measureUnit': 'mg/m³',
                'SORTING': 3,
                'uploadName': '非甲烷总烃浓度',
            },
            {
                'mStand': None,
                'factorCode': 'ga38',
                'uploadCode': 'STATE_ga38',
                'sStand': None,
                'dataType': 1,
                'factorType': 3,
                'lStand': None,
                'measureUnit': None,
                'SORTING': 7,
                'uploadName': '风机状态',
            },
            {
                'mStand': None,
                'factorCode': 'ga41',
                'uploadCode': 'STATE_ga41',
                'sStand': None,
                'dataType': 1,
                'factorType': 4,
                'lStand': None,
                'measureUnit': None,
                'SORTING': 8,
                'uploadName': '净化器状态',
            },
        ],
    }

    response = requests.post(
        'http://219.146.67.221:23111/dcloud-server/realUpdata/queryRealUpdateRegionCodeList',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )

    print('大气餐饮油烟—监控点-实时数据：'+response.text)
    return response

def mainSpider():
    global bean, datetimeTemp
    air_db: Session = next(get_air_db())

    response = getPointInfo()
    resp = json.loads(response.text)
    for r in range(len(resp["data"]['rows'])):
        dataBean = resp["data"]['rows'][r]
        print('列表第'+str(r+1) +'条数据：'+ str(dataBean))

        baseBean = TAirCateringRealtime.TAirCateringRealtime
        if (dataBean['dateTime'] != None):
            dataBean['dateTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(dataBean['dateTime'] / 1000))

        table = getBean(baseBean, dataBean)

        try:
            air_db.query(baseBean).filter(
                baseBean.COMPANY_NAME == dataBean['enterShort'],
                baseBean.STATION_ID == dataBean['stationId'],
                baseBean.STATION_ID == dataBean['dateTime']
            ).delete()
            air_db.add(table)
            air_db.commit()
        except Exception as e:
            print('大气餐饮油烟—监控点-异常'+str(e))
            continue
    air_db.close()


## 渣土车智能抓拍系统-》违规管理-》违规记录
if __name__ == '__main__':
    logger.success("大气餐饮油烟—监控点-采集开始...")
    mainSpider()
    logger.success("大气餐饮油烟—监控点-采集结束!")


