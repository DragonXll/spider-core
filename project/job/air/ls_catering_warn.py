#-- coding:UTF-8 --
import time
import argparse

from sqlalchemy.orm import Session
from database.mysql import get_air_db
from util import h
import requests
import json
from mod.catering import TAirCateringWarn
from core import logger
from datetime import datetime, timedelta

h._init()

## 监测数据
def getBean(baseBean, dataBean, dataBeanDetails):
    logger.info("====="+str(dataBeanDetails))
    difference =  datetime.strptime(dataBeanDetails['endTime'],"%Y-%m-%d %H:%M") - datetime.strptime(dataBeanDetails['startTime'],"%Y-%m-%d %H:%M")
    logger.info("====="+str(difference))
    return baseBean(
        COMPANY_NAME = dataBean['enterShort'], #监控点名称（餐厅名称）
        # AREA_CODE = dataBean['areaName'],# 区域编码
        AREA_NAME=dataBean['areaName'],  # 区域名称
        STATION_ID = dataBean['stationId'],#排口ID
        STATION_NAME = dataBean['stationName'],#排口名称
        MEASURED_INDEX = dataBeanDetails['eventName'],#监测指标
        # EXCEEDING_DURATION= dataBeanDetails[''],  # 超标时长
        START_TIME = dataBeanDetails['startTime'],  # 开始时间
        END_TIME = dataBeanDetails['endTime'], # 结束时间
        ALARM_STATUS = dataBeanDetails['alarmState'], # 报警状态
        PURIFIER_ON_TIME =  dataBeanDetails['purTime'],# 净化器开启时长
        PURIFIER_FAULT_TIME =  dataBeanDetails['purFaultTime'],# 净化器故障时长
        EXCESS_REASON =  dataBeanDetails['overReason'],# 超标原因


        SYS_CITY_CODE="370200000000",
        SYS_COUNTY_CODE="370212000000",
    )

cookies= h.buildCookies_ls_catering()
headers = h.buildHeader_ls_catering()

def getDetailMinute(stationId, start, end ):
    json_data = {
        'isRunAlarm': 'yes',
        'collation': 'asc',
        'stationId': [
            stationId,
        ],
        'startTime': start,
        'endTime': end,
        'dataType': '1',
        'alarmType': 'over_again',
        'factorCode': '',
        'page': 1,
        'limit': 999,
    }

    response = requests.post(
        'http://219.146.67.221:23111/dcloud-server/alarm/enterAlarmEvent',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    print('大气餐饮油烟—分钟数据-详细信息：' + response.text)
    return response
def getPointInfo(start, end):
    json_data = {
        'regionCode': '370212',
        'startTime': start,
        'endTime': end,
        'monitoringType': '',
        'overReason': '',
        'areaId': '',
        'enterSize': '',
        'cookingStyle': '',
        'enterType': '',
        'order': '',
        'orderBy': '',
        'stationMonitorType': '',
        'enterName': '',
        'page': 1,
        'limit': 999,
        'nationalStateCode': '',
        'nationalRangeCode': '',
    }

    response = requests.post(
        'http://219.146.67.221:23111/dcloud-base/supervise/overalarm/alarmList',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    print('大气餐饮油烟—监控点-信息：'+response.text)
    return response

def mainSpider(start, end):
    global bean, datetimeTemp
    air_db: Session = next(get_air_db())

    response = getPointInfo(start, end)
    resp = json.loads(response.text)
    for r in range(len(resp["data"]['rows'])):
        dataBean = resp["data"]['rows'][r]
        print('列表第'+str(r+1) +'条数据：'+ str(dataBean))
        responseDetails = getDetailMinute(dataBean['stationId'],start, end)
        respDetails = json.loads(responseDetails.text)

        for r in range(len(respDetails["data"]['rows'])):
            dataBeanDetails = respDetails["data"]['rows'][r]


            baseBean = TAirCateringWarn.TAirCateringWarn
            table = getBean(baseBean, dataBean, dataBeanDetails)

            air_db.query(baseBean).filter(
                                    baseBean.START_TIME == dataBeanDetails['startTime'],
                                    baseBean.END_TIME == dataBeanDetails['endTime'],
                                    baseBean.MEASURED_INDEX == dataBeanDetails['eventName'],
                                    baseBean.STATION_ID == dataBean['stationId']
                                ).delete()
            air_db.add(table)
    air_db.commit()
    air_db.close()


## 渣土车智能抓拍系统-》违规管理-》违规记录
if __name__ == '__main__':
    logger.success("大气餐饮油烟—监控点-采集开始...")

    current_date = datetime.now()
    global start, end
    beforeTime = current_date - timedelta(minutes=2)
    start = beforeTime.strftime("%Y-%m-%d %H:00:00")
    end = current_date.strftime("%Y-%m-%d %H:00:00")
    start = '2024-11-01'
    end  = '2024-11-12'

    mainSpider(start, end)
    logger.success("大气餐饮油烟—监控点-采集结束!")


