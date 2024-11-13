#-- coding:UTF-8 --
import time
import argparse

from sqlalchemy.orm import Session
from database.mysql import get_air_db
from util import h
import requests
import json
from mod.catering import TAirCateringPoint
from core import logger

h._init()
global enterSpider

## 监测数据
def getBean(baseBean, dataBean):
    return baseBean(
        CREDIT_NO = '',    #'统一社会信用代码'
        COMPANY_NAME_ALL = dataBean['enterName'], #监控点名称（餐厅名称）
        COMPANY_NAME = dataBean['enterShort'],  # 监控点名称（餐厅名称）
        AREA_CODE = '',#区域编码
        AREA_NAME = dataBean['areaName'],#区域名称
        STATION_ID = dataBean['id'],#排口ID
        STATION_CODE =dataBean['stationCode'], #排口编码
        STATION_NAME = dataBean['stationName'],#排口名称
        LONGITUDE = enterSpider[dataBean['enterShort']]['longitude'],#中心经度
        LATITUDE = enterSpider[dataBean['enterShort']]['latitude'],#中心纬度

        SYS_CITY_CODE="370200000000",
        SYS_COUNTY_CODE="370212000000",
    )

cookies= h.buildCookies_ls_catering()
headers = h.buildHeader_ls_catering()
def getPointInfo(page):
    json_data = {
        'page': page,
        'limit': 15,
        'areaId': '',
        'regionCode': '370212',
        'enterSize': '',
        'cookingStyle': '',
        'enterId': '',
        'enterName': '',
        'purEnterName': '',
        'nationalStateCode': '',
        'nationalRangeCode': '',
    }

    response = requests.post(
        'http://219.146.67.221:23111/dcloud-base/station/queryStationInfo',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )

    print('大气餐饮油烟—监控点-信息：'+response.text)
    return response

def getEnterInfo():
    json_data = {
        'regionCode': '370212',
        'areaIds': '',
        'enterSize': '',
        'cookingStyle': '',
        'enterShort': '',
        'gkaState': '',
        'rawState': '',
    }

    response = requests.post(
        'http://219.146.67.221:23111/dcloud-base/enter/queryEnterList',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    print('大气餐饮油烟—企业-信息：'+response.text)
    return response

def enterSpider():
    response = getEnterInfo()
    resp = json.loads(response.text)
    print('大气餐饮油烟—企业-信息，size：'+str(len(resp["data"])))
    enter_dict = {}
    for r in range(len(resp["data"])):
        enterBean = resp["data"][r]
        xy = {}
        xy["longitude"] =  str(enterBean['longitude'])
        xy["latitude"] =  str(enterBean['latitude'])
        enter_dict[enterBean['enterShort']] = xy
    print('大气餐饮油烟—企业-信息，经纬度：'+str(enter_dict))
    return enter_dict


def mainSpider():
    global bean, datetimeTemp
    air_db: Session = next(get_air_db())

    # # 获取记录列表
    # response = getPointInfo(1)
    # # 处理异常
    # try:
    #     resp = json.loads(response.text)
    # except:
    #     getPointInfo()
    # print('列表数量：' +str(len(resp["data"]['rows'])))
    # 循环列表
    # int(resp["data"]['total'])
    for i in range(6):
        response = getPointInfo(i+1)
        resp = json.loads(response.text)
        print('列表第' + str(i+1) + '页数据开始！' )
        for r in range(len(resp["data"]['rows'])):
            dataBean = resp["data"]['rows'][r]
            print('列表第'+str(r+1) +'条数据：'+ str(dataBean))

            baseBean = TAirCateringPoint.TAirCateringPoint
            table = getBean(baseBean, dataBean)

            air_db.query(baseBean).filter(
                                      baseBean.COMPANY_NAME_ALL == dataBean['enterName'],
                                      baseBean.STATION_ID == dataBean['id']
                                    ).delete()
            air_db.add(table)
    air_db.commit()
    air_db.close()


## 渣土车智能抓拍系统-》违规管理-》违规记录
if __name__ == '__main__':
    logger.success("大气餐饮油烟—监控点-采集开始...")
    ## 采集企业数据经纬度
    enterSpider = enterSpider()
    ## 采集站点数据
    mainSpider()
    logger.success("大气餐饮油烟—监控点-采集结束!")


