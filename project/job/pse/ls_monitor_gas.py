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
from mod import TPseMonitorGasHour
from mod import TPseMonitorGasDay
from mod import TPseMonitorGasMonth
from mod import TPseMonitorGasYear
from core import logger
from datetime import datetime, timedelta

h._init()

## 监测数据
def getGasBean(bean, resp, out, r):
    return bean(MONITOR_TIME=datetimeTemp,
             CREDIT_NO=out.CREDIT_NO,
             COMPANY_NAME=resp["rows"][r]['entName'],
             OUTPOINT_ID=out.OUTPOINT_CODE,
             OUTPOINT_TYPE=out.PSE_TYPE,
             OUTPOINT_NAME=resp["rows"][r]['subName'],

             PID_201=toFloat(resp["rows"][r]['pid_201']),
             VAL_201=toFloat(resp["rows"][r]['val2_201']),
             CVT_201=toFloat(resp["rows"][r]['cvt_201']),
             STAND_201=toFloat(resp["rows"][r]['stand_201']),
             EX_201=toFloat(resp["rows"][r]['ex_201']),
             STATUS_201=toFloat(resp["rows"][r]['state_201']),

             PID_203=toFloat(resp["rows"][r]['pid_203']),
             VAL_203=toFloat(resp["rows"][r]['val2_203']),
             CVT_203=toFloat(resp["rows"][r]['cvt_203']),
             STAND_203=toFloat(resp["rows"][r]['stand_203']),
             EX_203=toFloat(resp["rows"][r]['ex_203']),
             STATUS_203=toFloat(resp["rows"][r]['state_203']),

             PID_207=toFloat(resp["rows"][r]['pid_207']),
             VAL_207=toFloat(resp["rows"][r]['val2_207']),
             CVT_207=toFloat(resp["rows"][r]['cvt_207']),
             STAND_207=toFloat(resp["rows"][r]['stand_207']),
             EX_207=toFloat(resp["rows"][r]['ex_207']),
             STATUS_207=toFloat(resp["rows"][r]['state_207']),

             PID_205=toFloat(resp["rows"][r]['pid_205']),
             VAL_205=toFloat(resp["rows"][r]['val2_205']),
             CVT_205=toFloat(resp["rows"][r]['cvt_205']),
             STAND_205=toFloat(resp["rows"][r]['stand_205']),
             EX_205=toFloat(resp["rows"][r]['ex_205']),

             PID_221=toFloat(resp["rows"][r]['pid_221']),
             VAL_221=toFloat(resp["rows"][r]['val2_221']),
             CVT_221=toFloat(resp["rows"][r]['cvt_221']),
             STAND_221=toFloat(resp["rows"][r]['stand_221']),
             EX_221=toFloat(resp["rows"][r]['ex_221']),

             PID_222=toFloat(resp["rows"][r]['pid_222']),
             VAL_222=toFloat(resp["rows"][r]['val2_222']),
             CVT_222=toFloat(resp["rows"][r]['cvt_222']),
             STAND_222=toFloat(resp["rows"][r]['stand_222']),
             EX_222=toFloat(resp["rows"][r]['ex_222']),

             VAL_209=toFloat(resp["rows"][r]['val2_209']),
             VAL_210=toFloat(resp["rows"][r]['val2_210']),
             VAL_211=toFloat(resp["rows"][r]['val2_211']),

             SYS_CITY_CODE="370200000000",
             SYS_COUNTY_CODE="370212000000",
             )

def getGasBeanDay(bean, resp, out, r):
    return bean(MONITOR_TIME=datetimeTemp,
             CREDIT_NO=out.CREDIT_NO,
             COMPANY_NAME=resp["rows"][r]['entName'],
             OUTPOINT_ID=out.OUTPOINT_CODE,
             OUTPOINT_TYPE=out.PSE_TYPE,
             OUTPOINT_NAME=resp["rows"][r]['subName'],

             PID_201=toFloat(resp["rows"][r]['pid_201']),
             VAL_201=toFloat(resp["rows"][r]['val2_201']),
             CVT_201=toFloat(resp["rows"][r]['cvt_201']),
             STAND_201=toFloat(resp["rows"][r]['stand_201']),
             EX_201=toFloat(resp["rows"][r]['ex_201']),
             # STATUS_201=toFloat(resp["rows"][r]['state_201']),

             PID_203=toFloat(resp["rows"][r]['pid_203']),
             VAL_203=toFloat(resp["rows"][r]['val2_203']),
             CVT_203=toFloat(resp["rows"][r]['cvt_203']),
             STAND_203=toFloat(resp["rows"][r]['stand_203']),
             EX_203=toFloat(resp["rows"][r]['ex_203']),
             # STATUS_203=toFloat(resp["rows"][r]['state_203']),

             PID_207=toFloat(resp["rows"][r]['pid_207']),
             VAL_207=toFloat(resp["rows"][r]['val2_207']),
             CVT_207=toFloat(resp["rows"][r]['cvt_207']),
             STAND_207=toFloat(resp["rows"][r]['stand_207']),
             EX_207=toFloat(resp["rows"][r]['ex_207']),
             # STATUS_207=toFloat(resp["rows"][r]['state_207']),

             PID_205=toFloat(resp["rows"][r]['pid_205']),
             VAL_205=toFloat(resp["rows"][r]['val2_205']),
             CVT_205=toFloat(resp["rows"][r]['cvt_205']),
             STAND_205=toFloat(resp["rows"][r]['stand_205']),
             EX_205=toFloat(resp["rows"][r]['ex_205']),

             PID_221=toFloat(resp["rows"][r]['pid_221']),
             VAL_221=toFloat(resp["rows"][r]['val2_221']),
             CVT_221=toFloat(resp["rows"][r]['cvt_221']),
             STAND_221=toFloat(resp["rows"][r]['stand_221']),
             EX_221=toFloat(resp["rows"][r]['ex_221']),

             PID_222=toFloat(resp["rows"][r]['pid_222']),
             VAL_222=toFloat(resp["rows"][r]['val2_222']),
             CVT_222=toFloat(resp["rows"][r]['cvt_222']),
             STAND_222=toFloat(resp["rows"][r]['stand_222']),
             EX_222=toFloat(resp["rows"][r]['ex_222']),

             VAL_209=toFloat(resp["rows"][r]['val2_209']),
             VAL_210=toFloat(resp["rows"][r]['val2_210']),
             VAL_211=toFloat(resp["rows"][r]['val2_211']),

             SYS_CITY_CODE="370200000000",
             SYS_COUNTY_CODE="370212000000",
             )


def gas(status, start, end, index):
    global bean, datetimeTemp
    logger.success("废气启动成功")
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
        dc_env_pse.t_pse_outpoint_gas w
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
            'multiCode': '201,203,207,205,221,222,210',
            'codes': '201,203,207,205,221,222,209,210,211',
            'showUpload': '0',
            'subtype': '6',
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
        localtime = time.localtime(time.time())
        for r in range(len(resp["rows"])):
            if resp["rows"][r]['DateTime']:
                if i == "1":
                    datetimeTemp = '{}:{}'.format(resp["rows"][r]['DateTime'], "00:00")
                if i == "2":
                    # yesterday = datetime.now() - timedelta(days=1)
                    # datetimeTemp = yesterday.strftime("%Y-%m-%d")
                    datetimeTemp = '{}:{}'.format(resp["rows"][r]['DateTime'], " 00:00:00")
                if i == "3":
                    # datetimeTemp = datetime.now().strftime("%Y-%m-01")
                    datetimeTemp = '{}:{}'.format(resp["rows"][r]['DateTime'], "-01 00:00:00")
                if i == "4":
                    # datetimeTemp = datetime.now().strftime("%Y-01-01")
                    datetimeTemp = '{}:{}'.format(resp["rows"][r]['DateTime'], "-01-01 00:00:00")
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

            if status == "2":
                if index == "1":
                    bean = TPseMonitorGasHour
                    table = getGasBean(bean, resp, out, r)
                if index == "2":
                    bean = TPseMonitorGasDay
                    table = getGasBeanDay(bean, resp, out, r)
                if index == "3":
                    bean = TPseMonitorGasMonth
                    table = getGasBeanDay(bean, resp, out, r)
                if index == "4":
                    bean = TPseMonitorGasYear
                    table = getGasBeanDay(bean, resp, out, r)


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
    status = ["2"]

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

