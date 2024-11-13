from util import h
from sqlalchemy.orm import Session
from database.mysql import get_db
from job.pse import ls_login
import requests
import json


## 查询分析-》联网备案情况列表-》联网点位明细
db: Session = next(get_db())


# 企业信息拉取 4 5 6 页
def getEnterpriseInfo(page):
    if h.get_value("ASP.NET_SessionId") is None:
        ls_login.inits()
    headers = h.buildHeader_ls()
    cookies = h.buildCookies()

    data = {
        'menuid': '29',
        'Method': 'GetGrid',
        'cityCode': '370402,370403,370404,370405,370406,370407,370481',
        'SubType': '6,51,52,64',
        'EnterpriseCode': '',
        'controllevels': '',
        'sharesub': 'false',
        'industry': '',
        'isadmincodeFlag': '0',
        'wrylx': '',
        'page': page,
        'rows': '600',
    }

    response = requests.post(
        'http://222.135.190.229:8006/Web6/ajax/Report/Statistics/Record/EntSubDetailAnalysis.ashx',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    return response.text


# 拉取企业详情
def getBasicInfo(ecode):
    if h.get_value("ASP.NET_SessionId") is None:
        ls_login.inits()
    headers = h.buildHeader_ls()
    cookies = h.buildCookies()

    data = {
        'Method': 'GetDetail',
        'action': 'basic',
        'ecode': ecode,
        'otherview': '1',
        'subid': '',
        'isCompared': '0',
        'version': '',
    }

    response = requests.post(
        'http://222.135.190.229:8006/zdjkbak/BasicInfo/ajax/EnterpriseInfo/BasicInfo/BasicInfo.ashx',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    return response.text


def save():
    for i in [1]:
        resp = getEnterpriseInfo(i)
        data = json.loads(resp)
        print('总共数量：' + str(len(data["rows"])))
        for rows in range(len(data["rows"])):
            if str(data["rows"][rows]["C0003_STNAME"]) == '市值':
                continue
            subType = data["rows"][rows]["SUBTYPE"]
            if str(subType) == 'VOCs':
                type = '3'
            elif str(subType) == '废水':
                type = '1'
            elif str(subType) == '污水厂':
                type = '4'
            elif str(subType) == '废气':
                type = '2'

            basicInfo = getBasicInfo(data["rows"][rows]["C0070_ENTERPRISE_CODE"])
            basicInfo = json.loads(basicInfo)
            db.execute(
                "replace into dc_env_base.t_pub_company_pse (CREDIT_NO,PSE_NAME,PSE_CODE,PSE_TYPE,PSE_STATUS,"
                "SYS_CITY_CODE,SYS_COUNTY_CODE"
                ") values ('{}','{}','{}','{}','{}','{}','{}');".format(
                    basicInfo["C0070_SOCIAL_CODE"]
                    , basicInfo["C0070_ENTERPRISE_NAME"], basicInfo["C0070_ENTERPRISE_CODE"], type,
                    "1",
                     "370200000000", "370212000000"
                ))
        db.commit()

## 青岛市环境监测监控系统v6.1-》查询分析-》联网备案情况报表-》联网点位明细-》企业名称
if __name__ == '__main__':
    save()
