from datetime import datetime, timedelta

from requests import Session

from database.mysql import get_water_db
from util import h
from job.pse import ls_login
import socket
import socks
import requests
import pymysql


def get_hour_data():
    socks.setdefaultproxy(socks.SOCKS5, "101.43.54.132", 9988)
    socket.socket = socks.socksocket

    h._init()
    if h.get_value("ASP.NET_SessionId") is None:
        ls_login.inits()

    cookies = {
        'ASP.NET_SessionId': str(h.get_value("ASP.NET_SessionId")).replace('ASP.NET_SessionId=', ''),
    }
    # cookies = {
    #     'ASP.NET_SessionId': str("ASP.NET_SessionId=0wuz5j1bv3l0blkl1xizue30").replace('ASP.NET_SessionId=', ''),
    # }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'ASP.NET_SessionId=iqokyeiot1krvyljumbzvpik',
        'Origin': 'http://222.135.190.229:8006',
        'Pragma': 'no-cache',
        'Referer': 'http://222.135.190.229:8006/ajax/RiverSection/QueryAnalysis/HistoryReportMultiSubs/HistoryReport.ashx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    now = datetime.now()
    start_time = now - timedelta(days=1)
    start_for = start_time.strftime('%Y-%m-%d')
    end_time = now
    end_for = end_time.strftime('%Y-%m-%d')
    data = {
        'Method': 'QueryHistoryReport',
        'subid': '16156',
        'start': start_for,
        'end': end_for,
        'sort': '1',
        'showValidate': '0',
        'index': '2',
        'codes': '316,311,314,302,315,463,465,301,313,466',
        'page': '1',
        'rows': '500',
    }

    import pymysql

    response = requests.post(
        'http://222.135.190.229:8006/ajax/RiverSection/QueryAnalysis/HistoryReportMultiSubs/HistoryReport.ashx',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    body = response.json()
    print(response.text)
    # connect = pymysql.connect(host='47.104.223.137',
    #                           port=13306,
    #                           user='root',
    #                           password='Xizheng123!',
    #                           db='dc_env_water',
    #                           charset='utf8')
    # cur = connect.cursor()
    cur: Session = next(get_water_db())
    sys_city_code = 370200000000
    sys_county_code = 370212000000

    for row in body['rows']:
        if str(row['SubName']).__contains__('张村河308国道桥'):
            sql = """replace INTO t_water_waste_hour (STATION_NAME, MONITOR_TIME, PH, WATER_TA, DO_VALUE, CODMN, NH3, TN,
                                             TP, COD, SYS_CITY_CODE, SYS_COUNTY_CODE)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(sql,
                        (row['SubName'], row['DateTime'] + ':00:00',
                         row.get('val_302') if row.get('val_302') != '' else 0,
                         row.get('val_301') if row.get('val_301') != '' else 0,
                         row.get('val_315') if row.get('val_315') != '' else 0,
                         row.get('val_314') if row.get('val_314') != '' else 0,
                         row.get('val_311') if row.get('val_311') != '' else 0,
                         row.get('val_466') if row.get('val_466') != '' else 0,
                         row.get('val_313') if row.get('val_313') != '' else 0,
                         row.get('val_316') if row.get('val_316') != '' else 0,
                         sys_city_code,
                         sys_county_code))
    cur.commit()
    cur.close()



def get_day_data():
    socks.setdefaultproxy(socks.SOCKS5, "101.43.54.132", 9988)
    socket.socket = socks.socksocket
    import requests
    h._init()
    if h.get_value("ASP.NET_SessionId") is None:
        ls_login.inits()

    cookies = {
        'ASP.NET_SessionId': str(h.get_value("ASP.NET_SessionId")).replace('ASP.NET_SessionId=', ''),
    }

    # cookies = {
    #     'ASP.NET_SessionId': str("ASP.NET_SessionId=0wuz5j1bv3l0blkl1xizue30").replace('ASP.NET_SessionId=', ''),
    # }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'ASP.NET_SessionId=iqokyeiot1krvyljumbzvpik',
        'Origin': 'http://222.135.190.229:8006',
        'Pragma': 'no-cache',
        'Referer': 'http://222.135.190.229:8006/ajax/RiverSection/QueryAnalysis/HistoryReportMultiSubs/HistoryReport.ashx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    now = datetime.now()
    start_time = now - timedelta(days=1)
    start_for = start_time.strftime('%Y-%m-%d')
    end_time = now
    end_for = end_time.strftime('%Y-%m-%d')
    data = {
        'Method': 'QueryHistoryReport',
        'subid': '16156',
        'start': start_for,
        'end': end_for,
        'sort': '1',
        'showValidate': '0',
        'index': '2',
        'codes': '316,311,314,302,315,463,465,301,313,466',
        'page': '1',
        'rows': '500',
    }

    import pymysql

    response = requests.post(
        'http://222.135.190.229:8006/ajax/RiverSection/QueryAnalysis/HistoryReportMultiSubs/HistoryReport.ashx',
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    body = response.json()
    print(response.text)
    # connect = pymysql.connect(host='47.104.223.137',
    #                           port=13306,
    #                           user='root',
    #                           password='Xizheng123!',
    #                           db='dc_env_water',
    #                           charset='utf8')
    cur: Session = next(get_water_db())
    # cur = connect.cursor()
    sys_city_code = 370200000000
    sys_county_code = 370212000000
    for row in body['rows']:
        if str(row['SubName']).__contains__('张村河308国道桥'):
            sql = """replace INTO t_water_waste_day (STATION_NAME, MONITOR_TIME, PH, WATER_TA, DO_VALUE, CODMN, NH3, TN,
                                             TP, COD, SYS_CITY_CODE, SYS_COUNTY_CODE)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(sql,
                        (row['SubName'], row['DateTime'] + ':00:00',
                         row.get('val_302') if row.get('val_302') != '' else 0,
                         row.get('val_301') if row.get('val_301') != '' else 0,
                         row.get('val_315') if row.get('val_315') != '' else 0,
                         row.get('val_314') if row.get('val_314') != '' else 0,
                         row.get('val_311') if row.get('val_311') != '' else 0,
                         row.get('val_466') if row.get('val_466') != '' else 0,
                         row.get('val_313') if row.get('val_313') != '' else 0,
                         row.get('val_316') if row.get('val_316') != '' else 0,
                         sys_city_code,
                         sys_county_code))
    cur.commit()
    cur.close()


if __name__ == '__main__':
    get_hour_data()
    # get_day_data()