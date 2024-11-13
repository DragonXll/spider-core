import time

from sqlalchemy.orm import Session
from database.mysql import get_db
from database.mysql import get_pse_db
from mod import PseOutpointGas
from mod import PseOutpointWater
from mod import PubCompanyPse
from util import h
from job.pse import ls_login
import requests
import json
from core import logger

h._init()

## 排口信息
def outlet(types, status, data):
    global Status
    logger.success("排口启动成功")
    db: Session = next(get_db())
    pse_db: Session = next(get_pse_db())
    if h.get_value("ASP.NET_SessionId") is None:
        ls_login.inits()
    headers = h.buildHeader_ls()
    cookies = h.buildCookies()

    response = requests.post(
        'http://222.135.190.229:8006/ajax/WasteGas/RealTime/RealTimeDataQUIDYN/RealTimeData.ashx',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    try:
        resp = json.loads(response.text)
    except:
        ls_login.inits()
        outlet()
    for r in range(len(resp["rows"])):
        pseCompany = db.query(PubCompanyPse) \
            .filter(PubCompanyPse.PSE_NAME == resp["rows"][r]['EnterpriseName'],
                    PubCompanyPse.PSE_TYPE == types).first()
        if resp["rows"][r]['Status'] == "在产":
            Status = 0
        if resp["rows"][r]['Status'] == "停止排放":
            Status = 1
        if resp["rows"][r]['Status'] == "停产":
            Status = 2
        if pseCompany is None:
            continue
        pseCompany.PSE_STATUS = Status
        db.commit()
        if status == 1:
            if types == 2 or types == 3:

                pse_db.add(PseOutpointGas(CREDIT_NO=pseCompany.CREDIT_NO, OUTPOINT_CODE=resp["rows"][r]['SubID']
                                          , OUTPOINT_NAME=resp["rows"][r]['SubName'], SYS_CITY_CODE="370200000000",
                                          SYS_COUNTY_CODE="370212000000"))
                pse_db.commit()
            else:
                pse_db.add(PseOutpointWater(CREDIT_NO=pseCompany.CREDIT_NO, OUTPOINT_CODE=resp["rows"][r]['SubID']
                                            , OUTPOINT_NAME=resp["rows"][r]['SubName'], SYS_CITY_CODE="370200000000",
                                          SYS_COUNTY_CODE="370212000000"))
                pse_db.commit()

def start(status):
    ##废水
    data = {
        'Method': 'QueryRealTimeData',
        'city': '0',
        'levels': '1,2,64,512',
        'manager': '',
        'codes': '316,311,313,466,302,494',
        'subname': '',
        'entstatus': '-1|3|2',
        'devicestatus': '-1',
        'typep': '51',
        'menuid': '41',
    }
    outlet(1, status, data)
    ##废气
    data = {
        'Method': 'QueryRealTimeData',
        'city': '0',
        'levels': '1,2,64,512',
        'manager': '',
        'codes': '201,203,207,205,221,222,546,545,209,210,211,525,527,526',
        'subname': '',
        'entstatus': '-1|3|5|4|2|6',
        'devicestatus': '-1',
        'typep': '6',
        'menuid': '41',
    }
    outlet(2, status, data)
    ##VOCS
    data = {
        'Method': 'QueryRealTimeData',
        'city': '0',
        'levels': '1,2,64,512',
        'manager': '',
        'codes': '383,216,214,376,209,210,211,525,526,527,299,220,126,357,129,130,145',
        'subname': '',
        'entstatus': '-1|2|3|5|4|6',
        'devicestatus': '-1',
        'typep': '64',
        'menuid': '41',
    }
    # outlet(3, status, data)
    ##污水厂
    data = {
        'Method': 'QueryRealTimeData',
        'city': '0',
        'levels': '1,2,64,512',
        'manager': '',
        'codes': '316,311,313,466,302,301,494',
        'subname': '',
        'entstatus': '-1|3|2',
        'devicestatus': '-1',
        'typep': '52',
        'menuid': '41',
    }
    # outlet(4, status, data)

## 青岛市环境监测监控系统v6.1-》实时监控-》废气｜废水｜污水厂｜VOCs
if __name__ == '__main__':
    start(1)
