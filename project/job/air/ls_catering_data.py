#-- coding:UTF-8 --
import time
import argparse

from sqlalchemy.orm import Session
from database.mysql import get_air_db
from util import h
import requests
import json
from mod.catering import TAirCateringMinute
from mod.catering import TAirCateringHour
from mod.catering import TAirCateringDay
from core import logger
from datetime import datetime, timedelta

h._init()

## 监测数据
def getBean(baseBean, dataBean, dataBeanDetails):
    return baseBean(
        CREDIT_NO = '',    #'统一社会信用代码'
        COMPANY_NAME = dataBean['enterShort'], #监控点名称（餐厅名称）
        STATION_ID = dataBean['stationId'],#排口ID
        STATION_NAME = dataBean['stationName'],#排口名称
        MONITOR_TIME = dataBeanDetails['DT'],#监测时间
        # DETECTION_STATUS = ,#检测状态（0：正常 1：超标 2：离线  3：冻结）
        # PURIFIER_STATUS = ,#净化器状态（0=不在线；1=在线）
        # FAN_STATUS = ,#风机状态（0=不在线；1=在线）
        A34041 = dataBeanDetails['AVG_ga23'],#油烟浓度（A34041）
        A01002 = dataBeanDetails['AVG_ga24'],#颗粒物（A01002）
        A01001 = dataBeanDetails['AVG_ga25'],#非甲烷总烃（A01001）
        # AREA_CODE = dataBean['areaName'],# 区域编码
        AREA_NAME = dataBean['areaName'],#区域名称

        SYS_CITY_CODE="370200000000",
        SYS_COUNTY_CODE="370212000000",
    )

cookies= h.buildCookies_ls_catering()
headers = h.buildHeader_ls_catering()

def getDetailMinute(stationId, start, end, cnType):
    params = {
        'page': '1',
        'limit': '12',
        'endTime': end,
        'startTime': start,
        'regionCode': '370212',
        'dataType': '1',
        'cnType': cnType,
        'stationId': stationId,
        'enterName': '',
        'stationName': '',
        'dialogTime': '',
        'isDetail': '1',
    }

    response = requests.post(
        'http://219.146.67.221:23111/dcloud-server/dataQuery/queryDataDetailData',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )
    print('大气餐饮油烟—分钟数据-详细信息：' + response.text)
    return response
def getPointInfo(start, end, cnType):
    params = {
        'page': '1',
        'limit': '999',
        'endTime': end,
        'startTime': start,
        'areaId': '',
        'cookingStyle': '',
        'regionCode': '370212',
        'enterId': '',
        'enterName': '',
        'cnType': cnType,
        'dataType': '1',
        'factorType': '1',
        'enterSize': '',
        'isDetail': '1',
        'sortField': '',
        'order': '',
        'jsxs': '',
        'dialogTime': '2024-10-29',
        'stationId': '',
        'showJsxs': '0',
    }

    response = requests.post(
        'http://219.146.67.221:23111/dcloud-server/dataQuery/queryDataQueryDto',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )

    print('大气餐饮油烟—监控点-信息：'+response.text)
    return response

def mainSpider(start, end, index, cnType):
    global bean, datetimeTemp
    air_db: Session = next(get_air_db())

    for i in range(6):
        response = getPointInfo(start, end, cnType)
        resp = json.loads(response.text)
        print('列表第' + str(i+1) + '页数据开始！' )
        for r in range(len(resp["data"]['rows'])):
            dataBean = resp["data"]['rows'][r]
            print('列表第'+str(r+1) +'条数据：'+ str(dataBean))
            responseDetails = getDetailMinute(dataBean['stationId'],start, end, cnType)
            respDetails = json.loads(responseDetails.text)

            for r in range(len(respDetails["data"]['rows'])):
                dataBeanDetails = respDetails["data"]['rows'][r]

                if index == "1":
                    baseBean = TAirCateringMinute.TAirCateringMinute
                if index == "2":
                    baseBean = TAirCateringHour.TAirCateringHour
                if index == "3":
                    baseBean = TAirCateringDay.TAirCateringDay

                table = getBean(baseBean, dataBean, dataBeanDetails)

                air_db.query(baseBean).filter(
                                          baseBean.MONITOR_TIME == dataBeanDetails['DT'],
                                          baseBean.STATION_ID == dataBean['stationId']
                                        ).delete()
                air_db.add(table)
    air_db.commit()
    air_db.close()


## 渣土车智能抓拍系统-》违规管理-》违规记录
if __name__ == '__main__':
    logger.success("大气餐饮油烟—监控点-采集开始...")
    parser = argparse.ArgumentParser(description='解析参数')
    parser.add_argument('--dateType', '-d', help='时间类型(1=分钟；2=小时；3=天；)')
    args = parser.parse_args()
    if (args.dateType == None):
        index = ["1"]
    else:
        index = [args.dateType]
    print('index：', index)

    current_date = datetime.now()
    for i in index:
        global start, end, cnType
        if i == "1":
            cnType = '2051'
            beforeTime = current_date - timedelta(minutes=2)
            start = beforeTime.strftime("%Y-%m-%d %H:00:00")
            end = current_date.strftime("%Y-%m-%d %H:00:00")
            start = '2024-11-11'
            end  = '2024-11-11'
        if i == "2":
            cnType = '2061'
            two_hours_ago = current_date - timedelta(hours=2)
            start = two_hours_ago.strftime("%Y-%m-%d %H:00:00")
            end = current_date.strftime("%Y-%m-%d %H:00:00")
            start = '2024-11-11'
            end = '2024-11-11'
        if i == "3":
            cnType = '2031'
            yesterday = current_date - timedelta(days=2)
            start = yesterday.strftime("%Y-%m-%d")
            end = current_date.strftime("%Y-%m-%d")
            start = '2024-10-30'
            end = '2024-11-30'

        mainSpider(start, end, i, cnType)
    logger.success("大气餐饮油烟—监控点-采集结束!")


