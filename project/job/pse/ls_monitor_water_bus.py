#-- coding:UTF-8 --
import time
import argparse

from sqlalchemy.orm import Session
from database.mysql import get_db
from database.mysql import get_pse_db
from util import h
from job.pse import ls_login
import requests
import json
from mod import PseMonitorWaterBus
from mod import PseMonitorWaterBusDay
from mod import PseMonitorWaterBusMonth
from mod import PseMonitorWaterBusYear
from core import logger
from datetime import datetime, timedelta

h._init()

## 监测数据
def saveBean(bean, resp, out, r):
    return bean(MONITOR_TIME=datetimeTemp,
             CREDIT_NO=out.CREDIT_NO,
             COMPANY_NAME=resp["rows"][r]['entName'],
             OUTPOINT_ID=out.OUTPOINT_CODE,
             OUTPOINT_TYPE=out.PSE_TYPE,
             OUTPOINT_NAME=resp["rows"][r]['subName'],

            VAL_316=toFloat(resp["rows"][r]['val_316']),
            STAND_316=toFloat(resp["rows"][r]['stand_316']),
            EX_316=toFloat(resp["rows"][r]['ex_316']),
            # SOURCE_316=toFloat(resp["rows"][r]['source_316']),
            STATUS_316=toFloat(resp["rows"][r]['state_316']),

            VAL_311=toFloat(resp["rows"][r]['val_311']),
            STAND_311=toFloat(resp["rows"][r]['stand_311']),
            EX_311=toFloat(resp["rows"][r]['ex_311']),
            # SOURCE_311=resp["rows"][r]['source_311'],
            STATUS_311=toFloat(resp["rows"][r]['state_311']),

            VAL_313=toFloat(resp["rows"][r]['val_313']),
            STAND_313=toFloat(resp["rows"][r]['stand_313']),
            EX_313=toFloat(resp["rows"][r]['ex_313']),
            # SOURCE_313=resp["rows"][r]['source_313'],
            STATUS_313=toFloat(resp["rows"][r]['state_313']),

            VAL_466=toFloat(resp["rows"][r]['val_466']),
            STAND_466=toFloat(resp["rows"][r]['stand_466']),
            EX_466=toFloat(resp["rows"][r]['ex_466']),
            # SOURCE_466=resp["rows"][r]['source_466'],
            STATUS_466=toFloat(resp["rows"][r]['state_466']),

            VAL_323=toFloat(resp["rows"][r]['val_323']),
            STAND_323=toFloat(resp["rows"][r]['stand_323']),
            EX_323=toFloat(resp["rows"][r]['ex_323']),
            # SOURCE_323=resp["rows"][r]['source_323'],
            STATUS_323=toFloat(resp["rows"][r]['state_323']),

            VAL_331=toFloat(resp["rows"][r]['val_331']),
            STAND_331=toFloat(resp["rows"][r]['stand_331']),
            EX_331=toFloat(resp["rows"][r]['ex_331']),
            # SOURCE_331=resp["rows"][r]['source_331'],
            STATUS_331=toFloat(resp["rows"][r]['state_331']),

            VAL_302=toFloat(resp["rows"][r]['val_302']),
            STAND_302=toFloat(resp["rows"][r]['stand_302']),
            EX_302=toFloat(resp["rows"][r]['ex_302']),
            # SOURCE_302=resp["rows"][r]['source_302'],
            STATUS_302=toFloat(resp["rows"][r]['state_302']),

            VAL_324=toFloat(resp["rows"][r]['val_324']),
            STAND_324=toFloat(resp["rows"][r]['stand_324']),
            EX_324=toFloat(resp["rows"][r]['ex_324']),
            # SOURCE_324=resp["rows"][r]['source_324'],
            STATUS_324=toFloat(resp["rows"][r]['state_324']),

            VAL_318=toFloat(resp["rows"][r]['val_318']),
            STAND_318=toFloat(resp["rows"][r]['stand_318']),
            EX_318=toFloat(resp["rows"][r]['ex_318']),
            # SOURCE_318=resp["rows"][r]['source_318'],
            STATUS_318=toFloat(resp["rows"][r]['state_318']),


            VAL_301=toFloat(resp["rows"][r]['val_301']),
            STAND_301=toFloat(resp["rows"][r]['stand_301']),
            EX_301=toFloat(resp["rows"][r]['ex_301']),
            # SOURCE_301=resp["rows"][r]['source_301'],
            STATUS_301=toFloat(resp["rows"][r]['state_301']),

            VAL_494=toFloat(resp["rows"][r]['val_494']),
            STAND_494=toFloat(resp["rows"][r]['stand_494']),
            EX_494=toFloat(resp["rows"][r]['ex_494']),
            # SOURCE_494=resp["rows"][r]['source_494'],
            STATUS_494=toFloat(resp["rows"][r]['state_494']),

             SYS_CITY_CODE="370200000000",
             SYS_COUNTY_CODE="370212000000",
             )


def gas(status, start, end, index):
    global bean, datetimeTemp
    logger.success("污水厂启动成功")
    if h.get_value("ASP.NET_SessionId") is None:
        ls_login.inits()
    headers = h.buildHeader_ls()
    db: Session = next(get_db())
    pse_db: Session = next(get_pse_db())
    outLat = db.execute("""
    SELECT
        w.`OUTPOINT_CODE` AS `OUTPOINT_CODE`,
        w.`CREDIT_NO` AS `CREDIT_NO`,
        w.`ID` AS `ID`,
        p.`PSE_TYPE` AS `PSE_TYPE` 
    FROM
        dc_env_pse.t_pse_outpoint_water w
        LEFT JOIN t_pub_company_pse p ON w.`CREDIT_NO` = p.`CREDIT_NO` 
    WHERE p.SYS_COUNTY_CODE = '370212000000' and 
        p.`PSE_TYPE` = 
""" + status).all()
    for out in outLat:
        cookies = h.buildCookies()
        data = {
            'Method': 'QueryHistoryReport',
            'subid': out.OUTPOINT_CODE,
            'subname': '',
            'start': start,
            'end': end,
            'index': index,
            'sort': '1',
            'sortAscCheck': '1',
            'showValidate': '1',
            'multiCode': '316,311,313,466,494',
            'codes': '316,311,313,466,302,323,331,324,318,301,494',
            'showUpload': '0',
            'subtype': '52',
            'page': '1',
            'rows': '100',
        }

        response = requests.post(
            'http://222.135.190.229:8006/ajax/WasteGas/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.ashx',
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )

        print(response.text)
        try:
            resp = json.loads(response.text)
        except:
            ls_login.inits()
            gas(status, start, end, index)
        for r in range(len(resp["rows"])):
            if resp["rows"][r]['DateTime']:
                if i == "1":
                    datetimeTemp = '{}:{}'.format(resp["rows"][r]['DateTime'], "00:00")
                if i == "2":
                    datetimeTemp = '{}:{}'.format(resp["rows"][r]['DateTime'], " 00:00:00")
                if i == "3":
                    datetimeTemp = '{}:{}'.format(resp["rows"][r]['DateTime'], "-01 00:00:00")
                if i == "4":
                    datetimeTemp = '{}:{}'.format(resp["rows"][r]['DateTime'], "-01-01 00:00:00")
            else:
                continue

            ## 保存对象
            if index == "1":
                bean = PseMonitorWaterBus
            if index == "2":
                bean = PseMonitorWaterBusDay
            if index == "3":
                bean = PseMonitorWaterBusMonth
            if index == "4":
                bean = PseMonitorWaterBusYear


            table = saveBean(bean, resp, out, r)


            pse_db.query(bean).filter(bean.MONITOR_TIME == datetimeTemp,
                                      bean.OUTPOINT_NAME == resp["rows"][r]['subName'],
                                      bean.COMPANY_NAME == resp["rows"][r]['entName']).delete()
            pse_db.add(table)
        pse_db.commit()
        pse_db.close()


def toFloat(value):
    if value == 'nonexist':
        return None
    try:
        return float(value)
    except ValueError:
        return value
    except TypeError:
        return None


def get_start_and_end_of_month(year, month):
    # 构建指定年份和月份的第一天
    start_date = datetime(year, month, 1)

    # 计算下个月的第一天，并减去一天得到本月的最后一天
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    end_date = next_month - timedelta(days=1)

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

## 青岛市环境监测监控系统v6.1-》查询分析-》历史数据
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='解析参数')
    parser.add_argument('--dateType', '-d', help='时间类型(1=小时；2=天；3=月；4=年)')
    args = parser.parse_args()
    if(args.dateType==None):
        # index = ["1","2","3","4"]
        index = ["1"]
    else:
        index = [args.dateType]
    print('index：', index)

    ## 1=废水；2=废气；3=废气VOC；4=污水厂
    status = ["4"]

    current_date = datetime.now()
    for s in status:
        for i in index:
            global start, end
            if i == "1":
                two_hours_ago = current_date - timedelta(hours=2)
                start = two_hours_ago.strftime("%Y-%m-%d %H:00:00")
                end = current_date.strftime("%Y-%m-%d %H:00:00")
            if i == "2":
                yesterday = current_date - timedelta(days=2)
                start = yesterday.strftime("%Y-%m-%d")
                end = current_date.strftime("%Y-%m-%d")
            if i == "3":
                # start = "2023-01-01"
                # end = "2023-12-31"
                beforeTime = current_date - timedelta(weeks=6)
                start = beforeTime.strftime("%Y-%m-01")
                end = current_date.strftime("%Y-%m-%d")
            if i == "4":
                # start = "2018-01-01"
                # end = "2023-12-31"
                beforeTime = current_date - timedelta(weeks=10)
                start = beforeTime.strftime("%Y-01-01")
                end = current_date.strftime("%Y-12-31")
            gas(s, start, end, i)

