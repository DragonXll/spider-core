#-- coding:UTF-8 --
import time
import argparse

from sqlalchemy.orm import Session
from database.mysql import get_db
from database.mysql import get_air_db
from util import h
from job.pse import ls_login
import requests
import json
from mod import TAirInspect
from core import logger
from datetime import datetime, timedelta

h._init()

## 监测数据
def getGasBean(bean, inspectBean, out):
    return bean(MONITOR_TIME=datetimeTemp,
             CREDIT_NO=out.CREDIT_NO,
             COMPANY_NAME=out.COMPANY_NAME,
             OUTPOINT_CODE=out.OUTPOINT_CODE,
             OUTPOINT_NAME=out.OUTPOINT_NAME,
             MONITOR_TYPE="监督性监测",

             PROJECT_NAME=toFloat(inspectBean["projectName"]),
             MONITOR_VALUE=toFloat(inspectBean["monitorVale"]),
             MONITOR_STANDARD=toFloat(inspectBean["monitorStand"]),
             IS_PASS=toFloat(inspectBean["isPass"]),

             SYS_CITY_CODE="370200000000",
             SYS_COUNTY_CODE="370212000000",
             )


def gasInspect(status, start, end, index):
    global bean, datetimeTemp   # projectName,monitorVale,monitorStand,isPass
    logger.success("自行监测-废气启动成功")
    if h.get_value("ASP.NET_SessionId") is None:
        ls_login.inits()
    headers = h.buildHeader_ls()
    db: Session = next(get_db())
    air_db: Session = next(get_air_db())
    outLat = db.execute("""
    SELECT
        w.`OUTPOINT_CODE` AS `OUTPOINT_CODE`,
        w.`OUTPOINT_NAME` AS `OUTPOINT_NAME`,
        w.`CREDIT_NO` AS `CREDIT_NO`,
        w.`ID` AS `ID`,
        p.`PSE_TYPE` AS `PSE_TYPE`,
        p.`PSE_NAME` AS `COMPANY_NAME`
    FROM
        dc_env_pse.t_pse_outpoint_gas w
        LEFT JOIN t_pub_company_pse p ON w.`CREDIT_NO` = p.`CREDIT_NO` 
    WHERE p.SYS_COUNTY_CODE = '370212000000' and 
        p.`PSE_TYPE` = 
""" + status).all()
    for out in outLat:
        factors = ["201","203","207"]
        factorsName = ["二氧化硫", "氮氧化物", "颗粒物"]
        for i in range(len(factors)):
            params = {
                'Method': 'GetHistoryTime_new',
                'strID': out.OUTPOINT_CODE,
                'itemCode': factors[i],
                'SubType': '6',
                'PollCode': '1',
            }

            response = requests.get(
                'http://fb.sdem.org.cn:8801/wryfb/ajax/WasteWaterGis/WasteWaterHandler.ashx',
                params=params,
                headers=headers,
                verify=False,
            )

            try:
                resp = json.loads(response.text)
            except:
                # login.inits()
                logger.info("公司\""+out.OUTPOINT_CODE+"\"无数据！")
                # gasInspect(status, start, end, index)
                break

            if(resp["Data"][0]["hourState"][0]=="停产"):
                break

            hourNum_0 = resp["Data"][0]['Time'][0].replace("时", "")
            rLen = len(resp["Data"][0]["Time"])
            for rOldIndex in range(rLen):
                r = rLen - rOldIndex - 1
                if(r<20):
                    continue
                inspectBean = {}
                hourNum = resp["Data"][0]['Time'][r].replace("时", "")
                if(int(hourNum) >= int(hourNum_0)):
                    yesterday = current_date - timedelta(days=1)
                    yesterday = yesterday.strftime("%Y-%m-%d")
                    if(int(hourNum) <10):
                        hourNum = "0"+hourNum
                    datetimeTemp = '{}:{}:{}'.format(yesterday, hourNum, "00:00")
                else:
                    yesterday = current_date - timedelta(days=0)
                    yesterday = yesterday.strftime("%Y-%m-%d")
                    datetimeTemp = '{}:{}:{}'.format(yesterday, hourNum, ":00:00")

                inspectBean["monitorTime"] = datetimeTemp
                inspectBean["projectName"] = factorsName[i]
                inspectBean["monitorVale"] = resp["Data"][0]["data"][r]
                inspectBean["monitorStand"] = resp["Data"][0]["stand"]
                if(resp["Data"][0]["hourState"][r] == '正常'):
                    inspectBean["isPass"] = 0
                elif(resp["Data"][0]["hourState"][r] == '超标'):
                    inspectBean["isPass"] = 1
                else:
                    inspectBean["isPass"] = -1

                bean = TAirInspect
                table = getGasBean(bean, inspectBean, out)

                air_db.query(bean).filter(bean.MONITOR_TIME == datetimeTemp,
                                          bean.OUTPOINT_CODE == out.OUTPOINT_CODE,
                                          bean.CREDIT_NO == out.CREDIT_NO,
                                          bean.PROJECT_NAME == inspectBean["projectName"]
                                          ).delete()
                air_db.add(table)
        air_db.commit()
        air_db.close()

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
                beforeTime = current_date - timedelta(weeks=6)
                start = beforeTime.strftime("%Y-%m-01")
                end = current_date.strftime("%Y-%m-%d")
            if i == "4":
                beforeTime = current_date - timedelta(weeks=10)
                start = beforeTime.strftime("%Y-01-01")
                end = current_date.strftime("%Y-12-31")
            gasInspect(s, start, end, i)

