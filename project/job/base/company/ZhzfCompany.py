import requests
import json

from sqlalchemy.orm import Session
from database.mysql import get_db
from database.mysql import get_system_db
from mod import TPubCompany
from mod import TPubCompanyTag
from mod import TPubCompanyZhzf


def getDataBean(bean, r):
    # if ('PWXKZBH' in r):
    #     bean.CREDIT_NO = r['PWXKZBH']
    # elif ('QYDLZH' in r):
    #     bean.CREDIT_NO = r['QYDLZH']
    # elif ('TYSHXYDM' in r):
    #     bean.CREDIT_NO = r['TYSHXYDM']
    # elif ('ZZJGDM' in r):
    #     bean.CREDIT_NO = r['ZZJGDM']
    # else:
    #     continue
    if ('FDDBR' in r):
        bean.LEGAL_NAME = r['FDDBR']
    if ('HBLXR' in r):
        bean.ENV_CONTACTS_NAME = r['HBLXR']
    if ('HBRLXDH' in r):
        bean.ENV_CONTACTS_TEL = r['HBRLXDH']
    if ('FRLXDH' in r):
        bean.TEL = r['FRLXDH']
    if ('DWDZ' in r):
        bean.ADDRESS = r['DWDZ']
    if ('HYMC' in r):
        bean.INDUSTRY_CATE_NAME = r['HYMC']
    if ('SCZTMC' in r):
        bean.COMPANY_STATUS = r['SCZTMC']
    if ('JD' in r):
        bean.LONGITUDE = r['JD']
    if ('WD' in r):
        bean.LATITUDE = r['WD']
    return bean(CREDIT_NO = r['TYSHXYDM'],
                CREDIT_NO_TRUE = r['TYSHXYDM'],
                COMPANY_NAME = r['WRYMC'],
                COMPANY_STATUS = bean.COMPANY_STATUS,
                # GROUP_NO = r[''],
                # IS_SUPER = r[''],
                # COMPANY_NAME_HISTORY = r[''],
                # COMPANY_TYPE = r[''],
                # SCOPE = r[''],
                # LEGAL_NO = r[''],
                LEGAL_NAME = bean.LEGAL_NAME,
                ENV_CONTACTS_NAME = bean.ENV_CONTACTS_NAME,
                ENV_CONTACTS_TEL = bean.ENV_CONTACTS_TEL,
                ADDRESS = bean.ADDRESS,
                LONGITUDE = bean.LONGITUDE,
                LATITUDE = bean.LATITUDE,
                TEL = bean.TEL,
                # FAX = r[''],
                # POSTAL_CODE = r[''],
                # EMAIL = r[''],
                # WEB_SITE = r[''],
                # INDUSTRY_CODE = r[''],
                # INDUSTRY_NAME = r[''],
                INDUSTRY_CATE_NAME = bean.INDUSTRY_CATE_NAME,
                # INDUSTRY_CATE2_NAME = r[''],
                # INDUSTRY_CATE3_NAME = r[''],
                # INDUSTRY_CATE4_NAME = r[''],
                # QUALIFICATION = r[''],
                # BUILD_DATE = r[''],
                # STOP_DATE = r[''],
                # DISTRICT_CODE = r[''    ],
                # DISTRICT_CODE_TRUE = r[''],
             SYS_CITY_CODE="370200000000",
             SYS_COUNTY_CODE="370212000000",
    )
def getDataBeanTag(bean, r,rd):
    return bean(CREDIT_NO =  r['TYSHXYDM'],
                TAG_NAME =  rd['BQZ'],
             SYS_CITY_CODE="370200000000",
             SYS_COUNTY_CODE="370212000000",
    )

def getDataBeanTagZhzf(bean, r):
    if ('WRYLBMC' in r):
        bean.PSE_CATE = r['WRYLBMC']
    return bean(CREDIT_NO = r['TYSHXYDM'],
                COMPANY_NAME=r['WRYMC'],
                PSE_CATE=bean.PSE_CATE,
             SYS_CITY_CODE="370200000000",
             SYS_COUNTY_CODE="370212000000",
    )

def login_getToken():
    system_db: Session = next(get_system_db())

    return "2F8096E0690784922EC95370793323E1";

def getSpiderData(accessToken):
    cookies = {
        'JSESSIONID': accessToken,
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'JSESSIONID=0E624C97C09EB86A10EAA6E23045745F',
        'Origin': 'http://103.239.155.242:9001',
        'Pragma': 'no-cache',
        'Referer': 'http://103.239.155.242:9001/zhzf/xxgl/wry/wrylist?random=0da3',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'authorizationparam': '25acc35ca77e443bbe7bd1826013bccd',
    }

    json_data = {
        'pageNum': 1,
        'pageSize': 10000,
        'searchObj': {
            'HYLX': [],
            'BQ_LIST': {},
            'QYHJSJFXDJ': [],
            'WRYLB': [],
            'SCZT': [],
            'SFWZ': [],
            'SFZX': [],
            'SFCYSJCC': [],
            'SSSF': '370000',
            'SSDS': '370200',
            'SSQX': '370212',
            'HYLXMC': '',
        },
    }

    response = requests.post(
        'http://103.239.155.242:9001/zhzf/tagsimpl/wrylist/queryWryList',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )

    resp = json.loads(response.text)
    return resp

def getDataDetails(accessToken,WRYBH):
    cookies = {
        'JSESSIONID': accessToken,
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'JSESSIONID=1BE84FC2EA97036B31BC273DA02713F6',
        'Pragma': 'no-cache',
        'Referer': 'http://103.239.155.242:9001/zhzf/xxgl/wry/item?WRYBH='+WRYBH,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'authorizationparam': '75a7fc120a6fee9dad982ed1faeaf7fa',
    }
    params = {
        'WRYBH': WRYBH,
    }

    response = requests.get(
        'http://103.239.155.242:9001/zhzf/tagsimpl/wrylist/getJbxx',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )

    resp = json.loads(response.text)
    return resp


def spider():
    base_db: Session = next(get_db())

    accessToken = login_getToken()
    print('access_token：',  accessToken)
    resp = getSpiderData(accessToken)
    print('response.size：', len(resp['list']))

    for i in range(0,len(resp['list'])):
        r = resp['list'][i]
        print('r：', r)

        ## 保存公司基本信息
        bean = TPubCompany
        creditNo = None
        if ('TYSHXYDM' in r):
            creditNo = r['TYSHXYDM']
        else:
            continue

        table = getDataBean(bean,r)
        print('bean.CREDIT_NO:', creditNo)
        base_db.query(bean).filter(bean.CREDIT_NO == r['TYSHXYDM'],
                                   bean.COMPANY_NAME == r['WRYMC'],
                                   bean.SYS_CITY_CODE == '370200000000',
                                   bean.SYS_COUNTY_CODE == '370212000000'
                                   ).delete()
        base_db.add(table)
        base_db.commit()

        ## 保存公司执法信息
        beanZhzf = TPubCompanyZhzf
        tableTab = getDataBeanTagZhzf(beanZhzf, r)
        base_db.query(beanZhzf).filter(beanZhzf.CREDIT_NO == r['TYSHXYDM'],
                                       beanZhzf.COMPANY_NAME == r['WRYMC'],
                                       beanZhzf.SYS_CITY_CODE == '370200000000',
                                       beanZhzf.SYS_COUNTY_CODE == '370212000000'
                                       ).delete()
        base_db.add(tableTab)
        base_db.commit()

        ## 保存标签
        beanTag = TPubCompanyTag
        for i in range(0, len(r['lstTags'])):
            rd = r['lstTags'][i]
            tableTab = getDataBeanTag(beanTag,r,rd)
            base_db.query(beanTag).filter(beanTag.CREDIT_NO == r['TYSHXYDM'],
                                          beanTag.TAG_NAME == rd['BQZ'],
                                          beanTag.SYS_CITY_CODE == '370200000000',
                                          beanTag.SYS_COUNTY_CODE == '370212000000'
                                          ).delete(synchronize_session=False)
            base_db.add(tableTab)
        base_db.commit()

    base_db.close()

## 山东省生态环境保护综合执法智慧监管系统-》数据资源中心-》一源一档
if __name__ == '__main__':
    global bean,creditNo
    spider()

