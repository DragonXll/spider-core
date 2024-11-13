#-- coding:UTF-8 --
import time

from sqlalchemy.orm import Session
from database.mysql import get_pse_db
from util import h
from job.pse import ls_login
import requests
import json
from mod import TPseMonitorGasHour
from core import logger

h._init()

## 监测数据
def getGasBean(bean, resp, r):
    return bean(MONITOR_TIME=datetimeTemp,
             # CREDIT_NO=out.CREDIT_NO,
            COMPANY_NAME=resp["rows"][r]['EnterpriseName'],
            OUTPOINT_ID=resp["rows"][r]['SubID'],
            OUTPOINT_TYPE=resp["rows"][r]['SubType'],
            OUTPOINT_NAME=resp["rows"][r]['SubName'],
            COMPANY_STATUS=resp["rows"][r]['Status'],
            DEVICE_STATUS=resp["rows"][r]['StatusDevice'],

            ##二氧化硫(mg/M3)
            PID_201=toFloat(resp["rows"][r]['pid_201']),
            CVT_201=toFloat(resp["rows"][r]['cvt_201']),  ##折算值
            STAND_201=toFloat(resp["rows"][r]['stand_201']), ##标准值
            CBBS_201=toFloat(resp["rows"][r]['cbbs_201']),  ##超标倍数
            PFL_201=toFloat(resp["rows"][r]['pfl_201']),  ##截止前一日排放量

            ##氮氧化物(mg/M3)
            PID_203=toFloat(resp["rows"][r]['pid_203']),
            CVT_203=toFloat(resp["rows"][r]['cvt_203']),
            STAND_203=toFloat(resp["rows"][r]['stand_203']),
            CBBS_203=toFloat(resp["rows"][r]['cbbs_203']),  ##超标倍数
            PFL_203=toFloat(resp["rows"][r]['pfl_203']),  ##截止前一日排放量
            ##颗粒物(mg/M3)
            PID_207=toFloat(resp["rows"][r]['pid_207']),
            CVT_207=toFloat(resp["rows"][r]['cvt_207']),
            STAND_207=toFloat(resp["rows"][r]['stand_207']),
            CBBS_207=toFloat(resp["rows"][r]['cbbs_207']),  ##超标倍数
            PFL_207=toFloat(resp["rows"][r]['pfl_207']),  ##截止前一日排放量
            ##一氧化碳(mg/M3)
            PID_205=toFloat(resp["rows"][r]['pid_205']),
            CVT_205=toFloat(resp["rows"][r]['cvt_205']),
            STAND_205=toFloat(resp["rows"][r]['stand_205']),
            CBBS_205=toFloat(resp["rows"][r]['cbbs_205']),  ##超标倍数
            PFL_205=toFloat(resp["rows"][r]['pfl_205']),  ##截止前一日排放量
            ##氯化氢(mg/M3)
            PID_221=toFloat(resp["rows"][r]['pid_221']),
            CVT_221=toFloat(resp["rows"][r]['cvt_221']),
            STAND_221=toFloat(resp["rows"][r]['stand_221']),
            CBBS_221=toFloat(resp["rows"][r]['cbbs_221']),  ##超标倍数
            ##氟化氢(mg/M3)
            PID_222=toFloat(resp["rows"][r]['pid_222']),
            CVT_222=toFloat(resp["rows"][r]['cvt_222']),
            STAND_222=toFloat(resp["rows"][r]['stand_222']),
            CBBS_222=toFloat(resp["rows"][r]['cbbs_222']),  ##超标倍数

            VAL_209=toFloat(resp["rows"][r]['val_209']),
            VAL_210=toFloat(resp["rows"][r]['val_210']),
            VAL_211=toFloat(resp["rows"][r]['val_211']),

            SYS_CITY_CODE="370200000000",
            SYS_COUNTY_CODE="370212000000",
            )


def gas(status):
    global outputType,bean, datetimeTemp
    logger.success("废气实时启动成功")
    pse_db: Session = next(get_pse_db())
    if h.get_value("ASP.NET_SessionId") is None:
        ls_login.inits()
    headers = h.buildHeader_ls()
    data = {
        'Method': 'QueryRealTimeData',
        'city': '0',
        'levels': '1,2,64,512',
        'manager': '',
        'codes': '201,203,207,205,221,222,225,546,545,209,210,211,525,527,526',
        'subname': '',
        'entstatus': '-1|3|5|4|2',
        'devicestatus': '-1',
        'typep': status,
        'menuid': '41',
    }

    response = requests.post(
        'http://222.135.190.229:8006/ajax/WasteGas/RealTime/RealTimeDataQUIDYN/RealTimeData.ashx',
        headers=headers,
        data=data,
        verify=False,
    )
    try:
        resp = json.loads(response.text)
    except:
        ls_login.inits()
        gas(status)
    localtime = time.localtime(time.time())

    for r in range(len(resp["rows"])):
        if resp["rows"][r]['DateTime']:
            datetimeTemp = '{}-{}:{}'.format(localtime[0], resp["rows"][r]['DateTime'], "00")
        else:
            datetimeTemp = time.strftime("%Y-%m-%d %H:00:00", time.localtime())

        if status == "6":
            bean = TPseMonitorGasHour
            outputType = 2

        table = getGasBean(bean, resp, r)
        table.__setattr__("OUTPOINT_TYPE", outputType)

        try:
            pse_db.query(bean).filter(bean.MONITOR_TIME == datetimeTemp,
                                      bean.OUTPOINT_NAME == resp["rows"][r]['SubName'],
                                      bean.COMPANY_NAME == resp["rows"][r]['orgName']).delete()
            pse_db.add(table)
            pse_db.commit()
        except Exception as e:
            pse_db.rollback()
            pse_db.close()
            pse_db: Session = next(get_pse_db())
            if "Duplicate entry" in str(e) :
                ##查询是否存在
                outLat2 = pse_db.execute("""
                           SELECT
                               ID
                           FROM 
                               dc_env_pse.t_pse_monitor_gas
                           WHERE
                               `MONITOR_TIME` =  \""""+table.MONITOR_TIME+"""\"
                               and `COMPANY_NAME` =  \""""+table.COMPANY_NAME+"""\"
                               and `OUTPOINT_ID` =   """+table.OUTPOINT_ID+"""
                               and `SYS_CITY_CODE` =   """+table.SYS_CITY_CODE+"""
                               and `SYS_COUNTY_CODE` =   """+table.SYS_COUNTY_CODE+"""
                       """).all()
                if len(outLat2) > 0:
                    table.__setattr__("ID", outLat2[0]['ID'])

                    pse_db.merge(table)
                    pse_db.commit()
            continue
        finally:
            pse_db.commit()
    pse_db.close()

def toFloat(value):
    if value == 'nonexist':
        return None
    if len(value) ==0 :
        return None
    try:
        return float(value)
    except ValueError:
        return value
    except TypeError:
        return None


if __name__ == '__main__':
    ## 6=废气；64=废气VOC
    status = ["6"]
    for s in status:
        gas(s)

