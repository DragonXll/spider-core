#-- coding:UTF-8 --
import time
import argparse

from sqlalchemy.orm import Session
from database.mysql import get_db
from database.mysql import get_pse_db
from util import h
from job.pse import zz_login
import requests
import json
from mod import TPseMonitorGasVocHour
from mod import TPseMonitorGasVocDay
from mod import TPseMonitorGasVocMonth
from mod import TPseMonitorGasVocYear
from core import logger
from datetime import datetime, timedelta

h._init()

## 监测数据
def getGasBean(bean, resp, out, r):
    return bean(MONITOR_TIME=datetimeTemp,
             CREDIT_NO=out.CREDIT_NO,
             COMPANY_NAME=resp["rows"][r]['entName'],
             OUTPOINT_TYPE=out.PSE_TYPE,
             OUTPOINT_ID=out.OUTPOINT_CODE,
             OUTPOINT_NAME=resp["rows"][r]['subName'],

             PID_220=toFloat(resp["rows"][r]['pid_220']),
             VAL_220=toFloat(resp["rows"][r]['val_220']),
             CVT_220=toFloat(resp["rows"][r]['cvt_220']),
             STAND_220=toFloat(resp["rows"][r]['stand_220']),
             EX_220=toFloat(resp["rows"][r]['ex_220']),

             PID_299=toFloat(resp["rows"][r]['pid_299']),
             VAL_299=toFloat(resp["rows"][r]['val_299']),
             CVT_299=toFloat(resp["rows"][r]['cvt_299']),
             STAND_299=toFloat(resp["rows"][r]['stand_299']),
             EX_299=toFloat(resp["rows"][r]['ex_299']),

             PID_383=toFloat(resp["rows"][r]['pid_383']),
             VAL_383=toFloat(resp["rows"][r]['val_383']),
             CVT_383=toFloat(resp["rows"][r]['cvt_383']),
             STAND_383=toFloat(resp["rows"][r]['stand_383']),
             EX_383=toFloat(resp["rows"][r]['ex_383']),

             PID_216=toFloat(resp["rows"][r]['pid_216']),
             VAL_216=toFloat(resp["rows"][r]['val2_216']),
             CVT_216=toFloat(resp["rows"][r]['cvt_216']),
             STAND_216=toFloat(resp["rows"][r]['stand_216']),
             EX_216=toFloat(resp["rows"][r]['ex_216']),

             PID_214=toFloat(resp["rows"][r]['pid_214']),
             VAL_214=toFloat(resp["rows"][r]['val_214']),
             CVT_214=toFloat(resp["rows"][r]['cvt_214']),
             STAND_214=toFloat(resp["rows"][r]['stand_214']),
             EX_214=toFloat(resp["rows"][r]['ex_214']),

             PID_376=toFloat(resp["rows"][r]['pid_376']),
             VAL_376=toFloat(resp["rows"][r]['val_376']),
             CVT_376=toFloat(resp["rows"][r]['cvt_376']),
             STAND_376=toFloat(resp["rows"][r]['stand_376']),
             EX_376=toFloat(resp["rows"][r]['ex_376']),

             VAL_209=toFloat(resp["rows"][r]['val_209']),
             VAL_210=toFloat(resp["rows"][r]['val_210']),
             VAL_211=toFloat(resp["rows"][r]['val_211']),

             SYS_CITY_CODE="370400000000",
             SYS_COUNTY_CODE="370402000000",
             )


def gas(status, start, end, index):
    global bean, datetimeTemp
    logger.success("废气启动成功")
    if h.get_value("ASP.NET_SessionId") is None:
        zz_login.inits()
    db: Session = next(get_db())
    pse_db: Session = next(get_pse_db())
    outLat = db.execute("""
    SELECT
        w.`OUTPOINT_CODE` AS `OUTPOINT_CODE`,
        w.`CREDIT_NO` AS `CREDIT_NO`,
        w.`ID` AS `ID`,
        p.`PSE_TYPE` AS `PSE_TYPE` 
    FROM
        dc_env_pse.t_pse_outpoint_gas w
        LEFT JOIN t_pub_company_pse p ON w.`CREDIT_NO` = p.`CREDIT_NO` 
    WHERE p.SYS_COUNTY_CODE = '370402000000' and 
        p.`PSE_TYPE` = 
""" + status).all()
    for out in outLat:
        headers = h.buildHeader_zz()
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
            'multiCode': '383,216,214,376,210',
            'codes': '383,216,214,376,209,210,211,525,526,527,299,220,230,207,126,357,129,130,145',
            'showUpload': '0',
            'subtype': '64',
            'page': '1',
            'rows': '100',
        }
        response = requests.post(
            'http://60.214.99.139:8006/ajax/WasteGas/QueryAnalysis/HistoryReportQUIDYN/HistoryReport.ashx',
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )

        print(response.text)
        try:
            resp = json.loads(response.text)
        except:
            zz_login.inits()
            gas(status, start, end, index)
        localtime = time.localtime(time.time())
        for r in range(len(resp["rows"])):
            if resp["rows"][r]['DateTime']:
                if i == "1":
                    datetimeTemp = '{}:{}'.format(resp["rows"][r]['DateTime'], "00:00")
                if i == "2":
                    yesterday = datetime.now() - timedelta(days=1)
                    datetimeTemp = yesterday.strftime("%Y-%m-%d")
                if i == "3":
                    datetimeTemp = datetime.now().strftime("%Y-%m-01")
                if i == "4":
                    datetimeTemp = datetime.now().strftime("%Y-01-01")
            else:
                if i == "1":
                    two_hours_ago = current_date - timedelta(hours=1)
                    datetimeTemp = two_hours_ago.strftime("%Y-%m-%d %H:00:00")
                if i == "2":
                    yesterday = datetime.now() - timedelta(days=1)
                    datetimeTemp = yesterday.strftime("%Y-%m-%d")
                if i == "3":
                    datetimeTemp = datetime.now().strftime("%Y-%m")
                if i == "4":
                    datetimeTemp = datetime.now().strftime("%Y")

            if status == "3":
                if index == "1":
                    bean = TPseMonitorGasVocHour
                if index == "2":
                    bean = TPseMonitorGasVocDay
                if index == "3":
                    bean = TPseMonitorGasVocMonth
                if index == "4":
                    bean = TPseMonitorGasVocYear

            table = getGasBean(bean, resp, out, r)
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

    ## 2=废气；3=废气VOC
    status = ["3"]

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
                beforeTime = current_date - timedelta(weeks=6)
                start = beforeTime.strftime("%Y-%m-01")
                end = current_date.strftime("%Y-%m-%d")
            if i == "4":
                beforeTime = current_date - timedelta(weeks=10)
                start = beforeTime.strftime("%Y-01-01")
                end = current_date.strftime("%Y-12-31")
            gas(s, start, end, i)

