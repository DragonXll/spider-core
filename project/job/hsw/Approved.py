import argparse
import decimal

import pymysql
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

import Common
from Login import Singleton, getSession
from core import config

# commited 提交
# pass 有效
# reject 退回
handle_status = {'commited': 1, 'pass': 2, 'reject': 3}
# 形态（1=固态；2=液态；3=气态
harm_form = {'固态': 1, '液态': 2, '气态': 3}
# 1=提交｜已提交；2=有效｜备案通过；3=退回｜备案退回
handle_status1 = {'备案通过': 1, '备案退回': 2, '已提交': 3, '编辑中': 4}
# 1=新产生利用处置；2=接收利用处置
store_type = {'R': 2, 'P': 1}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'SESSION=79d39b6e-8950-4755-a52e-30ba7a907445; Hm_lpvt_0aabb31005445bec1e2759bd1a8a8485=1690177015; DataCenter_TicketId=sys_ticket_8F5BA2E7-5B43-4B50-9DBA-1BDF0C6DBBC9; SECKEY_ABVK=IVOyJPsI7nV5ABhaXwLn8FuXHI6pLl0IiaVClWmJmJ0%3D; BMAP_SECKEY=X2NdJ1IRuOiJv3qnI6Pw9W1xgvRTzVa3TXoUxwdJFtrqiPwD-jHVknXDbgqdH_uga7rigPbuO4eh9WlgMhl8fU9IKwFuOak8McoNI60AGOB1y1nKFekg4jhIlT2nNDnUBxGOLgno13-A8Gekj-mWGIwZjJ1W50GSIBT_a8JcN4X-8C5Vl2S6vE5JvY4Ks3zj; Hm_lvt_0aabb31005445bec1e2759bd1a8a8485=1690180338,1690180625,1690180712,1690180860',
    'Origin': 'http://120.221.95.83:6080',
    'Referer': 'http://120.221.95.83:6080/main/view/declarationStatistic/monthlyStatisticsEpaView.html?entType=QYSX_CZ&ticketId=8F5BA2E7-5B43-4B50-9DBA-1BDF0C6DBBC9&orgId=2054298711623680&QUSERXZQ=TXXB6Y3dNakXV5&d=1690180853871&menuCode=JYYBCX&isShowDeclarationMonth=false',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def getDangerMonth(ticketId, session):
    params = {
        'ticketId': ticketId,
    }

    data = {
        'size': '50',
        'current': '1',
        'entName': '',
        'endDate': '',
        'beginDate': '',
        'busiStatus': '',
        'cantonCode': '',
        'cantonLevel': '',
        'type': 'view',
        'entType': 'QYSX_CZ',
        'enterpriseId': '',
        'industrySourceType': '',
        'provinceLevel': '',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declarationStatistic/listEpaDeclarationStatisticMonthly',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    danger_list = response.json()['data']
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in danger_list:
        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['enterpriseName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        # 查询是否已某个企业是否已有这个月的记录
        query_exsit = """select * from t_hsw_store_h_month where CREDIT_NO=%s and COMPANY_NAME = %s and MONITOR_DATE=%s"""
        cursorTarget.execute(query_exsit, [results1[0], item['enterpriseName'], item['time'] + '-01'])
        is_exsit = cursorTarget.fetchall()
        if len(is_exsit)==0:
            print('不存在'+results1[0], item['enterpriseName'], item['time'] + '-01')
            sql = '''insert into t_hsw_store_h_month ( CREDIT_NO, COMPANY_NAME, MONITOR_DATE, LAST_STORE_QTY, 
        CUR_STORE_QTY, OVER_STORE_QTY, GENE_QTY, FIX_QTY, TRANS_QTY, RECEIVE_QTY, DISPOSE_QTY, HANDLE_STATUS, 
        SYS_CITY_CODE, SYS_COUNTY_CODE ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
            insert = cursorTarget.execute(sql,
                                      [results1[0],
                                       item['enterpriseName'],
                                       item['time'] + '-01',
                                       item['lastInventoryQuantity'],
                                       item['inventoryQuantity'],
                                       item['inventoryQuantityOverYear'],
                                       item['generateQuantity'],
                                       item['adjustQuantity'],
                                       item['transferQuantity'],
                                       item['receiveQuantity'],
                                       item['useDisposalQuantity'],
                                       handle_status.setdefault(item['declarBusiStatus'])
                                       ])
            print(insert)
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getProduceDangerMonth(ticketId, session):
    params = {
        'ticketId': ticketId,
    }

    data = {
        'size': '2600',
        'current': '1',
        'entName': '',
        'endDate': '',
        'beginDate': '',
        'busiStatus': '',
        'cantonCode': '',
        'cantonLevel': '',
        'type': 'view',
        'entType': 'QYSX_CF',
        'enterpriseId': '',
        'industrySourceType': '',
        'provinceLevel': '',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declarationStatistic/listEpaDeclarationStatisticMonthly',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    danger_list = response.json()['data']
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in danger_list:
        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['enterpriseName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        if results1 is None:
            continue
        # 查询是否已某个企业是否已有这个月的记录
        query_exsit = """select * from t_hsw_store_h_month where CREDIT_NO=%s and COMPANY_NAME = %s and MONITOR_DATE=%s"""
        cursorTarget.execute(query_exsit, [results1[0], item['enterpriseName'], item['time'] + '-01'])
        is_exsit = cursorTarget.fetchall()
        if len(is_exsit) == 0:
            print('不存在' + results1[0], item['enterpriseName'], item['time'] + '-01')
            sql = '''insert into t_hsw_store_h_month (
                                                    CREDIT_NO,
                                                    COMPANY_NAME,
                                                    MONITOR_DATE,
                                                    LAST_STORE_QTY,
                                                    CUR_STORE_QTY,
                                                    OVER_STORE_QTY,
                                                    GENE_QTY,
                                                    FIX_QTY,
                                                    TRANS_QTY,
                                                    RECEIVE_QTY,
                                                    DISPOSE_QTY,
                                                    HANDLE_STATUS,
                                                    SYS_CITY_CODE,
                                                    SYS_COUNTY_CODE
                                                   ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
            insert = cursorTarget.execute(sql,
                                      [results1[0],
                                       item['enterpriseName'],
                                       item['time'] + '-01',
                                       item['lastInventoryQuantity'],
                                       item['inventoryQuantity'],
                                       item['inventoryQuantityOverYear'],
                                       item['generateQuantity'],
                                       item['adjustQuantity'],
                                       item['transferQuantity'],
                                       item['receiveQuantity'],
                                       item['useDisposalQuantity'],
                                       handle_status.setdefault(item['declarBusiStatus'])
                                       ])
            print(insert)
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getDangerMonthDetail(ticketId, session):
    params = {
        'ticketId': ticketId,
    }

    data = {
        'size': '50',
        'current': '1',
        'entName': '',
        'endDate': '',
        'beginDate': '',
        'busiStatus': '',
        'cantonCode': '',
        'cantonLevel': '',
        'type': 'view',
        'entType': 'QYSX_CZ',
        'enterpriseId': '',
        'industrySourceType': '',
        'provinceLevel': '',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declarationStatistic/listEpaDeclarationStatisticMonthly',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    danger_list = response.json()['data']
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in danger_list:
        params = {
            'ticketId': ticketId,
            'id': item['declarationId'],
            'type': '1',
            'time': item['time'],
            'entName': 'null',
            'enterpriseId': item['enterpriseId'],
        }
        print('执行')
        data = {
            'name': '',
            'wasteTypeCode': '',
            'wasteCode': '',
        }
        response = requests.post(
            'http://120.221.95.83:6080/declarationStatistic/showDetails',
            params=params,
            cookies=Common.getCookie(session),
            headers=headers,
            data=data,
            verify=False,
        )
        detail_list = response.json()['data']

        # 如果详情表存在该公司该时间则不录入
        query = """select * from t_hsw_store_h_month_detail where COMPANY_NAME = %s and MONITOR_DATE = %s"""
        cursorTarget.execute(query, [item['enterpriseName'], item['time'] + '-01'])
        results2 = cursorTarget.fetchall()
        if len(results2) != 0:
            continue

        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['enterpriseName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()

        for i in detail_list:
            print(i['pattern'])
            c_list = i['declarationGeneratedWasteStorageList']
            storageName = c_list[0]['storageName']
            lasteStorageQuantity = c_list[0]['lasteStorageQuantity']
            storageQuantity = c_list[0]['storageQuantity']
            overYearStorageQuantity = c_list[0]['overYearStorageQuantity']
            z_list = i['declarationGeneratedWasteDetailVOlist']
            useDisposalQuantity = 0
            for z in z_list:
                useDisposalQuantity += z['useDisposalQuantity']
            r_list = i['declarationGeneratedWasteSourceDetailVOList']
            receiveQuantity = 0
            for r in r_list:
                receiveQuantity += r['receiveQuantity']
            # 不可放入重复
            sql = '''insert into t_hsw_store_h_month_detail (                           
                                                CREDIT_NO,
                                                COMPANY_NAME,
                                                MONITOR_DATE,
                                                HSW_CATE,
                                                HSW_CATE_NAME,
                                                HSW_CODE,
                                                HSW_CODE_NAME,
                                                HSW_NAME,
                                                UNIT,
                                                HARM_NAME,
                                                HARM_FORM,
                                                HARM_TYPE,
                                                STORE_FACILITY,
                                                LAST_STORE_QTY,
                                                CUR_STORE_QTY,
                                                OVER_STORE_QTY,
                                                GENE_QTY,
                                                TRANS_QTY,
                                                RECEIVE_QTY,
                                                FIX_QTY,
                                                DISPOSE_QTY,
                                                SYS_CITY_CODE,
                                                SYS_COUNTY_CODE
                                                       ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
            insert = cursorTarget.execute(sql,
                                          [
                                              results1[0],
                                              item['enterpriseName'],
                                              item['time'] + '-01',
                                              i['wasteTypeCode'],
                                              i['name'],
                                              i['wasteCode'],
                                              i['description'],
                                              i['name'],
                                              i['unit'],
                                              i['harmfulComponents'],
                                              harm_form.setdefault(i['pattern']),
                                              i['features'],
                                              storageName,
                                              lasteStorageQuantity,
                                              storageQuantity,
                                              overYearStorageQuantity,
                                              i['generation'],
                                              useDisposalQuantity,
                                              receiveQuantity,
                                              i['adjustCalcQuantity'],
                                              i['useDisposalQuantity']
                                          ])
            print(insert)
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getProduceDangerMonthDetail(ticketId, session):
    params = {
        'ticketId': ticketId,
    }

    data = {
        'size': '1000',
        'current': '1',
        'entName': '',
        'endDate': '',
        'beginDate': '',
        'busiStatus': '',
        'cantonCode': '',
        'cantonLevel': '',
        'type': 'view',
        'entType': 'QYSX_CF',
        'enterpriseId': '',
        'industrySourceType': '',
        'provinceLevel': '',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declarationStatistic/listEpaDeclarationStatisticMonthly',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    danger_list = response.json()['data']
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in danger_list:
        # if item['time'].startswith('2022'):
        #     continue
        # if item['time'].startswith('2021'):
        #     continue
        params = {
            'ticketId': ticketId,
            'id': item['declarationId'],
            'type': '1',
            'time': item['time'],
            'entName': 'null',
            'enterpriseId': item['enterpriseId'],
        }

        data = {
            'name': '',
            'wasteTypeCode': '',
            'wasteCode': '',
        }
        response = requests.post(
            'http://120.221.95.83:6080/declarationStatistic/showDetails',
            params=params,
            cookies=Common.getCookie(session),
            headers=headers,
            data=data,
            verify=False,
        )
        detail_list = response.json()['data']
        if detail_list is None:
            continue
        # 如果详情表存在该公司该时间则不录入
        query = """select * from t_hsw_store_h_month_detail where COMPANY_NAME = %s and MONITOR_DATE = %s"""
        cursorTarget.execute(query, [item['enterpriseName'], item['time'] + '-01'])
        results2 = cursorTarget.fetchall()
        if len(results2) != 0:
            continue

        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['enterpriseName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        if results1 is None:
            continue
        for i in detail_list:
            print(i['pattern'])
            c_list = i['declarationGeneratedWasteStorageList']
            storageName = ''
            lasteStorageQuantity = 0
            storageQuantity = 0
            overYearStorageQuantity = 0
            if len(c_list) != 0:
                storageName = c_list[0]['storageName']
                lasteStorageQuantity = c_list[0]['lasteStorageQuantity']
                storageQuantity = c_list[0]['storageQuantity']
                overYearStorageQuantity = c_list[0]['overYearStorageQuantity']
            z_list = i['declarationGeneratedWasteDetailVOlist']
            useDisposalQuantity = 0
            for z in z_list:
                useDisposalQuantity += z['useDisposalQuantity']
            r_list = i['declarationGeneratedWasteSourceDetailVOList']
            receiveQuantity = 0
            for r in r_list:
                receiveQuantity += r['receiveQuantity']
            # 不可放入重复
            sql = '''insert into t_hsw_store_h_month_detail (                           
                                                    CREDIT_NO,
                                                    COMPANY_NAME,
                                                    MONITOR_DATE,
                                                    HSW_CATE,
                                                    HSW_CATE_NAME,
                                                    HSW_CODE,
                                                    HSW_CODE_NAME,
                                                    HSW_NAME,
                                                    UNIT,
                                                    HARM_NAME,
                                                    HARM_FORM,
                                                    HARM_TYPE,
                                                    STORE_FACILITY,
                                                    LAST_STORE_QTY,
                                                    CUR_STORE_QTY,
                                                    OVER_STORE_QTY,
                                                    GENE_QTY,
                                                    TRANS_QTY,
                                                    RECEIVE_QTY,
                                                    FIX_QTY,
                                                    DISPOSE_QTY,
                                                    SYS_CITY_CODE,
                                                    SYS_COUNTY_CODE
                                                           ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
            insert = cursorTarget.execute(sql,
                                          [
                                              results1[0],
                                              item['enterpriseName'],
                                              item['time'] + '-01',
                                              i['wasteTypeCode'],
                                              i['name'],
                                              i['wasteCode'],
                                              i['description'],
                                              i['name'],
                                              i['unit'],
                                              i['harmfulComponents'],
                                              harm_form.setdefault(i['pattern']),
                                              i['features'],
                                              storageName,
                                              lasteStorageQuantity,
                                              storageQuantity,
                                              overYearStorageQuantity,
                                              i['generation'],
                                              useDisposalQuantity,
                                              receiveQuantity,
                                              i['adjustCalcQuantity'],
                                              i['useDisposalQuantity']
                                          ])
            print(insert)
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getDangerYear(ticketId, session):
    params = {
        'ticketId': ticketId,
        'enterprise_attribute': [
            'QYSX_CZ',
            'QYSX_CZ',
        ],
        'wasteType': '',
    }

    data = {
        'draw': '1',
        'columns[0][data]': 'a$entName',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'a$licenceNo',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'false',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'a$type',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'a$declarationTime',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'false',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'ee$instName',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'false',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'u$userName',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'false',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'a$edited_time',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'false',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'a$status',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'false',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'columns[8][data]': 'a$id',
        'columns[8][name]': '',
        'columns[8][searchable]': 'true',
        'columns[8][orderable]': 'false',
        'columns[8][search][value]': '',
        'columns[8][search][regex]': 'false',
        'start': '0',
        'length': '70',
        'search[value]': '',
        'search[regex]': 'false',
        'conditions': '{"enterpriseName":"","status":"select","areaLevel":"","areaCode":"","cantonCode":"370212","cantonLevel":"3","instId":"2054298711623680","declarationTime":""}',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declaration/epaViewListForJson',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    result_list = response.json()['data']
    print(result_list)
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in result_list:
        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['a$entName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        data = {
            'ticketId': ticketId,
            'declarationId': item['a$id'],
        }
        response1 = requests.post(
            'http://120.221.95.83:6080/declarationGeneratedWaste/listForJson',
            cookies=Common.getCookie(session),
            headers=headers,
            data=data,
            verify=False,
        )
        x_list = response1.json()['data']
        generation = 0
        shiftOutSumQuantity = 0
        capacityPastYear = 0
        receiveSumQuantity = 0
        capacity = 0
        disposalSumQuantity = 0
        for x in x_list:
            if x['generation'] is not None:
                generation += decimal.Decimal(x['generation'])
            if x['shiftOutSumQuantity'] is not None:
                shiftOutSumQuantity += decimal.Decimal(x['shiftOutSumQuantity'])
            if x['capacityPastYear'] is not None:
                capacityPastYear += decimal.Decimal(x['capacityPastYear'])
            if x['receiveSumQuantity'] is not None:
                receiveSumQuantity += decimal.Decimal(x['receiveSumQuantity'])
            if x['capacity'] is not None:
                capacity += decimal.Decimal(x['capacity'])
            if x['disposalSumQuantity'] is not None:
                disposalSumQuantity += decimal.Decimal(x['disposalSumQuantity'])
        sql = '''insert into t_hsw_store_h_year (
                                                        CREDIT_NO,
                                                        COMPANY_NAME,
                                                        MONITOR_DATE,
                                                        GENE_QTY,
                                                        LAST_STORE_QTY,
                                                        CUR_STORE_QTY,
                                                        DISPOSE_QTY,
                                                        TRANS_QTY,
                                                        RECEIVE_QTY,
                                                        HANDLE_STATUS,
                                                        SYS_CITY_CODE,
                                                        SYS_COUNTY_CODE
                                                       ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
        insert = cursorTarget.execute(sql,
                                      [results1[0],
                                       item['a$entName'],
                                       item['a$declarationTime'],
                                       generation,
                                       capacityPastYear,
                                       capacity,
                                       disposalSumQuantity,
                                       shiftOutSumQuantity,
                                       receiveSumQuantity,
                                       handle_status1.setdefault(item['a$status'])
                                       ])
        print(insert)
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getProduceDangerYear(ticketId, session):
    params = {
        'ticketId': ticketId,
        'enterprise_attribute': [
            'QYSX_CF',
            'QYSX_CF',
        ],
        'wasteType': '1',
    }

    data = {
        'draw': '1',
        'columns[0][data]': 'aa$entName',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'a$type',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'false',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'a$declarationTime',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'ee$instName',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'false',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'u$userName',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'false',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'a$edited_time',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'false',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'a$status',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'false',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'a$id',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'false',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'start': '0',
        'length': '866',
        'search[value]': '',
        'search[regex]': 'false',
        'conditions': '{"enterpriseName":"","status":"select","season":"select","areaLevel":"","areaCode":"","areaName":"","cantonCode":"370212","cantonLevel":"3","instId":"2054298711623680","entName":"","EntType":"","type":""}',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declaration/epaViewListForJson',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    result_list = response.json()['data']
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in result_list:
        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['a$entName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        if results1 is None:
            continue
        data = {
            'ticketId': ticketId,
            'declarationId': item['a$id'],
        }
        response1 = requests.post(
            'http://120.221.95.83:6080/declarationGeneratedWaste/listForJson',
            cookies=Common.getCookie(session),
            headers=headers,
            data=data,
            verify=False,
        )
        x_list = response1.json()['data']
        generation = 0
        shiftOutSumQuantity = 0
        capacityPastYear = 0
        receiveSumQuantity = 0
        capacity = 0
        disposalSumQuantity = 0
        for x in x_list:
            if x['generation'] is not None:
                generation += decimal.Decimal(x['generation'])
            if x['shiftOutSumQuantity'] is not None:
                shiftOutSumQuantity += decimal.Decimal(x['shiftOutSumQuantity'])
            if x['capacityPastYear'] is not None:
                capacityPastYear += decimal.Decimal(x['capacityPastYear'])
            if x['receiveSumQuantity'] is not None:
                receiveSumQuantity += decimal.Decimal(x['receiveSumQuantity'])
            if x['capacity'] is not None:
                capacity += decimal.Decimal(x['capacity'])
            if x['disposalSumQuantity'] is not None:
                disposalSumQuantity += decimal.Decimal(x['disposalSumQuantity'])
        sql = '''insert into t_hsw_store_h_year (
                                                        CREDIT_NO,
                                                        COMPANY_NAME,
                                                        MONITOR_DATE,
                                                        GENE_QTY,
                                                        LAST_STORE_QTY,
                                                        CUR_STORE_QTY,
                                                        DISPOSE_QTY,
                                                        TRANS_QTY,
                                                        RECEIVE_QTY,
                                                        HANDLE_STATUS,
                                                        SYS_CITY_CODE,
                                                        SYS_COUNTY_CODE
                                                       ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
        insert = cursorTarget.execute(sql,
                                      [results1[0],
                                       item['a$entName'],
                                       item['a$declarationTime'],
                                       generation,
                                       capacityPastYear,
                                       capacity,
                                       disposalSumQuantity,
                                       shiftOutSumQuantity,
                                       receiveSumQuantity,
                                       handle_status1.setdefault(item['a$status'])
                                       ])
        print(insert)
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getDangerYearDetail(ticketId, session):
    params = {
        'ticketId': ticketId,
        'enterprise_attribute': [
            'QYSX_CZ',
            'QYSX_CZ',
        ],
        'wasteType': '',
    }

    data = {
        'draw': '1',
        'columns[0][data]': 'a$entName',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'a$licenceNo',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'false',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'a$type',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'a$declarationTime',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'false',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'ee$instName',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'false',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'u$userName',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'false',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'a$edited_time',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'false',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'a$status',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'false',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'columns[8][data]': 'a$id',
        'columns[8][name]': '',
        'columns[8][searchable]': 'true',
        'columns[8][orderable]': 'false',
        'columns[8][search][value]': '',
        'columns[8][search][regex]': 'false',
        'start': '0',
        'length': '70',
        'search[value]': '',
        'search[regex]': 'false',
        'conditions': '{"enterpriseName":"","status":"select","areaLevel":"","areaCode":"","cantonCode":"370212","cantonLevel":"3","instId":"2054298711623680","declarationTime":""}',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declaration/epaViewListForJson',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    result_list = response.json()['data']
    print(result_list)
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in result_list:
        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['a$entName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        data = {
            'ticketId': ticketId,
            'declarationId': item['a$id'],
        }
        response1 = requests.post(
            'http://120.221.95.83:6080/declarationGeneratedWaste/listForJson',
            cookies=Common.getCookie(session),
            headers=headers,
            data=data,
            verify=False,
        )
        x_list = response1.json()['data']
        for x in x_list:
            data = {
                'id': x['id'],
                'ticketId': ticketId,
            }

            response = requests.post(
                'http://120.221.95.83:6080/declarationGeneratedWaste/edit',
                cookies=Common.getCookie(session),
                headers=headers,
                data=data,
                verify=False,
            )
            featuresText = response.json()['data']['featuresText']
            patternText = response.json()['data']['patternText']
            sql = '''insert into t_hsw_store_h_year_detail (
                                                        CREDIT_NO,
                                                        COMPANY_NAME,
                                                        MONITOR_DATE,
                                                        HSW_CATE,
                                                        HSW_CATE_NAME,
                                                        HSW_CODE,
                                                        HSW_NAME,
                                                        GENE_QTY,
                                                        LAST_STORE_QTY,
                                                        CUR_STORE_QTY,
                                                        DISPOSE_QTY,
                                                        TRANS_QTY,
                                                        RECEIVE_QTY,
                                                        HARM_FORM,
                                                        HARM_TYPE,
                                                        STORE_TYPE, 
                                                        SYS_CITY_CODE,
                                                        SYS_COUNTY_CODE
                                                       ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
            insert = cursorTarget.execute(sql,
                                          [results1[0],
                                           item['a$entName'],
                                           item['a$declarationTime'],
                                           x['wasteTypeCode'],
                                           x['generatedWasteName'],
                                           x['wasteCode'],
                                           x['generatedWasteName'],
                                           x['generation'],
                                           x['capacityPastYear'],
                                           x['capacity'],
                                           x['disposalSumQuantity'],
                                           x['shiftOutSumQuantity'],
                                           x['receiveSumQuantity'],
                                           harm_form.setdefault(patternText),
                                           featuresText,
                                           store_type.setdefault(x['wasteSource'], 0)
                                           ])
            print(insert)
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getProduceDangerYearDetail(ticketId, session):
    params = {
        'ticketId': ticketId,
        'enterprise_attribute': [
            'QYSX_CF',
            'QYSX_CF',
        ],
        'wasteType': '1',
    }

    data = {
        'draw': '1',
        'columns[0][data]': 'aa$entName',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'a$type',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'false',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'a$declarationTime',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'ee$instName',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'false',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'u$userName',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'false',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'a$edited_time',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'false',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'a$status',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'false',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'a$id',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'false',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'start': '0',
        'length': '50',
        'search[value]': '',
        'search[regex]': 'false',
        'conditions': '{"enterpriseName":"","status":"select","season":"select","areaLevel":"","areaCode":"","areaName":"","cantonCode":"370212","cantonLevel":"3","instId":"2054298711623680","entName":"","EntType":"","type":""}',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declaration/epaViewListForJson',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    result_list = response.json()['data']
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in result_list:
        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['a$entName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        if results1 is None:
            continue
        data = {
            'ticketId': ticketId,
            'declarationId': item['a$id'],
        }
        response1 = requests.post(
            'http://120.221.95.83:6080/declarationGeneratedWaste/listForJson',
            cookies=Common.getCookie(session),
            headers=headers,
            data=data,
            verify=False,
        )
        x_list = response1.json()['data']
        for x in x_list:
            data = {
                'id': x['id'],
                'ticketId': ticketId,
            }

            response = requests.post(
                'http://120.221.95.83:6080/declarationGeneratedWaste/edit',
                cookies=Common.getCookie(session),
                headers=headers,
                data=data,
                verify=False,
            )
            featuresText = response.json()['data']['featuresText']
            patternText = response.json()['data']['patternText']
            sql = '''insert into t_hsw_store_h_year_detail (
                                                                    CREDIT_NO,
                                                                    COMPANY_NAME,
                                                                    MONITOR_DATE,
                                                                    HSW_CATE,
                                                                    HSW_CATE_NAME,
                                                                    HSW_CODE,
                                                                    HSW_NAME,
                                                                    GENE_QTY,
                                                                    LAST_STORE_QTY,
                                                                    CUR_STORE_QTY,
                                                                    DISPOSE_QTY,
                                                                    TRANS_QTY,
                                                                    RECEIVE_QTY,
                                                                    HARM_FORM,
                                                                    HARM_TYPE,
                                                                    STORE_TYPE, 
                                                                    SYS_CITY_CODE,
                                                                    SYS_COUNTY_CODE
                                                                   ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
            insert = cursorTarget.execute(sql,
                                          [results1[0],
                                           item['a$entName'],
                                           item['a$declarationTime'],
                                           x['wasteTypeCode'],
                                           x['generatedWasteName'],
                                           x['wasteCode'],
                                           x['generatedWasteName'],
                                           x['generation'],
                                           x['capacityPastYear'],
                                           x['capacity'],
                                           x['disposalSumQuantity'],
                                           x['shiftOutSumQuantity'],
                                           x['receiveSumQuantity'],
                                           harm_form.setdefault(patternText),
                                           featuresText,
                                           store_type.setdefault(x['wasteSource'], 0)
                                           ])
            print(insert)
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getSolidYear(ticketId, session):
    params = {
        'ticketId': ticketId,
        'enterprise_attribute': [
            'QYSX_CF',
            'QYSX_CF',
        ],
        'wasteType': '2',
    }

    data = {
        'draw': '1',
        'columns[0][data]': 'aa$entName',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'a$type',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'false',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'a$declarationTime',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'ee$instName',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'false',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'u$userName',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'false',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'a$edited_time',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'false',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'a$status',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'false',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'a$id',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'false',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'start': '0',
        'length': '200',
        'search[value]': '',
        'search[regex]': 'false',
        'conditions': '{"enterpriseName":"","status":"select","season":"select","areaLevel":"","areaCode":"","areaName":"","cantonCode":"370212","cantonLevel":"3","instId":"2054298711623680","exportType":"","entName":"","type":""}',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declaration/epaViewListForJson',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    result_list = response.json()['data']
    print(result_list)
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in result_list:
        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['a$entName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        if results1 is None:
            continue
        data = {
            'ticketId': ticketId,
            'declarationId': item['a$id'],
        }
        response1 = requests.post(
            'http://120.221.95.83:6080/declarationGeneratedWaste/listForJson',
            cookies=Common.getCookie(session),
            headers=headers,
            data=data,
            verify=False,
        )
        x_list = response1.json()['data']
        generation = 0
        shiftOutSumQuantity = 0
        capacityPastYear = 0
        receiveSumQuantity = 0
        capacity = 0
        disposalSumQuantity = 0
        for x in x_list:
            if x['generation'] is not None:
                generation += decimal.Decimal(x['generation'])
            if x['shiftOutSumQuantity'] is not None:
                shiftOutSumQuantity += decimal.Decimal(x['shiftOutSumQuantity'])
            if x['capacityPastYear'] is not None:
                capacityPastYear += decimal.Decimal(x['capacityPastYear'])
            if x['receiveSumQuantity'] is not None:
                receiveSumQuantity += decimal.Decimal(x['receiveSumQuantity'])
            if x['capacity'] is not None:
                capacity += decimal.Decimal(x['capacity'])
            if x['disposalSumQuantity'] is not None:
                disposalSumQuantity += decimal.Decimal(x['disposalSumQuantity'])
        sql = '''insert into t_hsw_store_s_year (
                                                           CREDIT_NO,
                                                           COMPANY_NAME,
                                                           MONITOR_DATE,
                                                           GENE_QTY,
                                                           TRANS_QTY,
                                                           RECEIVE_QTY,
                                                           LAST_STORE_QTY,
                                                           CUR_STORE_QTY,
                                                           SELF_DISPOSE_QTY,                              
                                                           SYS_CITY_CODE,
                                                           SYS_COUNTY_CODE
                                                          ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
        insert = cursorTarget.execute(sql,
                                      [results1[0],
                                       item['a$entName'],
                                       item['a$declarationTime'],
                                       generation,
                                       shiftOutSumQuantity,
                                       receiveSumQuantity,
                                       capacityPastYear,
                                       capacity,
                                       disposalSumQuantity
                                       ])
        print(insert)
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getProduceSolidYear(ticketId, session):
    params = {
        'ticketId': ticketId,
        'enterprise_attribute': [
            'QYSX_CZ',
            'QYSX_CZ',
        ],
        'wasteType': '2',
    }

    data = {
        'draw': '1',
        'columns[0][data]': 'aa$entName',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'a$type',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'false',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'a$declarationTime',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'ee$instName',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'false',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'u$userName',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'false',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'a$edited_time',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'false',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'a$status',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'false',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'a$id',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'false',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'start': '0',
        'length': '160',
        'search[value]': '',
        'search[regex]': 'false',
        'conditions': '{"enterpriseName":"","status":"3","season":"select","areaLevel":"","areaCode":"","areaName":"","cantonCode":"370212","cantonLevel":"3","instId":"2054298711623680","exportType":"","entName":"","type":""}',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declaration/epaViewListForJson',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    result_list = response.json()['data']
    print(result_list)
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in result_list:
        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['a$entName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        if results1 is None:
            continue
        data = {
            'ticketId': ticketId,
            'declarationId': item['a$id'],
        }
        response1 = requests.post(
            'http://120.221.95.83:6080/declarationGeneratedWaste/listForJson',
            cookies=Common.getCookie(session),
            headers=headers,
            data=data,
            verify=False,
        )
        x_list = response1.json()['data']
        generation = 0
        shiftOutSumQuantity = 0
        capacityPastYear = 0
        receiveSumQuantity = 0
        capacity = 0
        disposalSumQuantity = 0
        for x in x_list:
            if x['generation'] is not None:
                generation += decimal.Decimal(x['generation'])
            if x['shiftOutSumQuantity'] is not None:
                shiftOutSumQuantity += decimal.Decimal(x['shiftOutSumQuantity'])
            if x['capacityPastYear'] is not None:
                capacityPastYear += decimal.Decimal(x['capacityPastYear'])
            if x['receiveSumQuantity'] is not None:
                receiveSumQuantity += decimal.Decimal(x['receiveSumQuantity'])
            if x['capacity'] is not None:
                capacity += decimal.Decimal(x['capacity'])
            if x['disposalSumQuantity'] is not None:
                disposalSumQuantity += decimal.Decimal(x['disposalSumQuantity'])
        query1 = """select * from t_hsw_store_s_year where COMPANY_NAME = %s and CREDIT_NO=%s"""
        cursorTarget.execute(query1, [item['a$entName'], results1[0]])
        # 获取所有记录列表
        results2 = cursorTarget.fetchall()
        if len(results2) == 0:
            sql = '''insert into t_hsw_store_s_year (
                                                              CREDIT_NO,
                                                              COMPANY_NAME,
                                                              MONITOR_DATE,
                                                              GENE_QTY,
                                                              TRANS_QTY,
                                                              RECEIVE_QTY,
                                                              LAST_STORE_QTY,
                                                              CUR_STORE_QTY,
                                                              SELF_DISPOSE_QTY,                              
                                                              SYS_CITY_CODE,
                                                              SYS_COUNTY_CODE
                                                             ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
            insert = cursorTarget.execute(sql,
                                          [results1[0],
                                           item['a$entName'],
                                           item['a$declarationTime'],
                                           generation,
                                           shiftOutSumQuantity,
                                           receiveSumQuantity,
                                           capacityPastYear,
                                           capacity,
                                           disposalSumQuantity
                                           ])
            print(insert)
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getSolidYearDetail(ticketId, session):
    params = {
        'ticketId': ticketId,
        'enterprise_attribute': [
            'QYSX_CF',
            'QYSX_CF',
        ],
        'wasteType': '2',
    }

    data = {
        'draw': '1',
        'columns[0][data]': 'aa$entName',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'a$type',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'false',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'a$declarationTime',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'ee$instName',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'false',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'u$userName',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'false',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'a$edited_time',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'false',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'a$status',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'false',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'a$id',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'false',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'start': '0',
        'length': '200',
        'search[value]': '',
        'search[regex]': 'false',
        'conditions': '{"enterpriseName":"","status":"select","season":"select","areaLevel":"","areaCode":"","areaName":"","cantonCode":"370212","cantonLevel":"3","instId":"2054298711623680","exportType":"","entName":"","type":""}',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declaration/epaViewListForJson',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    result_list = response.json()['data']
    print(result_list)
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in result_list:
        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['a$entName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        if results1 is None:
            continue
        data = {
            'ticketId': ticketId,
            'declarationId': item['a$id'],
        }
        response1 = requests.post(
            'http://120.221.95.83:6080/declarationGeneratedWaste/listForJson',
            cookies=Common.getCookie(session),
            headers=headers,
            data=data,
            verify=False,
        )
        x_list = response1.json()['data']
        for x in x_list:
            query = """select * from t_hsw_store_s_year_detail where CREDIT_NO=%s and COMPANY_NAME = %s
                                                                    and MONITOR_DATE = %s and HSW_CATE = %s
                                                                    and HSW_CATE_NAME = %s and HSW_CODE_NAME = %s
                                                                    and HSW_NAME = %s"""
            cursorTarget.execute(query, [results1[0],
                                         item['a$entName'],
                                         item['a$declarationTime'],
                                         x['wasteTypeCode'],
                                         x['generatedWasteName'],
                                         x['wasteCode'],
                                         x['generatedWasteName']
                                         ])
            # 获取所有记录列表
            results2 = cursorTarget.fetchall()
            if len(results2) == 0:
                sql = '''insert into t_hsw_store_s_year_detail (CREDIT_NO,
                                                           COMPANY_NAME,
                                                           MONITOR_DATE,
                                                           HSW_CATE,
                                                           HSW_CATE_NAME,
                                                           HSW_CODE_NAME,
                                                           HSW_NAME,
                                                           GENE_QTY,
                                                           TRANS_QTY,
                                                           CUR_STORE_QTY,
                                                           SELF_DISPOSE_QTY,
                                                           RECEIVE_QTY,
                                                           LAST_STORE_QTY,                         
                                                           SYS_CITY_CODE,
                                                           SYS_COUNTY_CODE
                                                          )values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
                insert = cursorTarget.execute(sql,
                                              [results1[0],
                                               item['a$entName'],
                                               item['a$declarationTime'],
                                               x['wasteTypeCode'],
                                               x['generatedWasteName'],
                                               x['wasteCode'],
                                               x['generatedWasteName'],
                                               x['generation'],
                                               x['shiftOutSumQuantity'],
                                               x['storageSumQuantity'],
                                               x['disposalSumQuantity'],
                                               x['receiveSumQuantity'],
                                               x['capacityPastYear']
                                               ])
                print(insert)
                conn.commit()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


def getProduceSolidYearDetail(ticketId, session):
    params = {
        'ticketId': ticketId,
        'enterprise_attribute': [
            'QYSX_CZ',
            'QYSX_CZ',
        ],
        'wasteType': '2',
    }

    data = {
        'draw': '1',
        'columns[0][data]': 'aa$entName',
        'columns[0][name]': '',
        'columns[0][searchable]': 'true',
        'columns[0][orderable]': 'false',
        'columns[0][search][value]': '',
        'columns[0][search][regex]': 'false',
        'columns[1][data]': 'a$type',
        'columns[1][name]': '',
        'columns[1][searchable]': 'true',
        'columns[1][orderable]': 'false',
        'columns[1][search][value]': '',
        'columns[1][search][regex]': 'false',
        'columns[2][data]': 'a$declarationTime',
        'columns[2][name]': '',
        'columns[2][searchable]': 'true',
        'columns[2][orderable]': 'false',
        'columns[2][search][value]': '',
        'columns[2][search][regex]': 'false',
        'columns[3][data]': 'ee$instName',
        'columns[3][name]': '',
        'columns[3][searchable]': 'true',
        'columns[3][orderable]': 'false',
        'columns[3][search][value]': '',
        'columns[3][search][regex]': 'false',
        'columns[4][data]': 'u$userName',
        'columns[4][name]': '',
        'columns[4][searchable]': 'true',
        'columns[4][orderable]': 'false',
        'columns[4][search][value]': '',
        'columns[4][search][regex]': 'false',
        'columns[5][data]': 'a$edited_time',
        'columns[5][name]': '',
        'columns[5][searchable]': 'true',
        'columns[5][orderable]': 'false',
        'columns[5][search][value]': '',
        'columns[5][search][regex]': 'false',
        'columns[6][data]': 'a$status',
        'columns[6][name]': '',
        'columns[6][searchable]': 'true',
        'columns[6][orderable]': 'false',
        'columns[6][search][value]': '',
        'columns[6][search][regex]': 'false',
        'columns[7][data]': 'a$id',
        'columns[7][name]': '',
        'columns[7][searchable]': 'true',
        'columns[7][orderable]': 'false',
        'columns[7][search][value]': '',
        'columns[7][search][regex]': 'false',
        'start': '0',
        'length': '200',
        'search[value]': '',
        'search[regex]': 'false',
        'conditions': '{"enterpriseName":"","status":"select","season":"select","areaLevel":"","areaCode":"","areaName":"","cantonCode":"370212","cantonLevel":"3","instId":"2054298711623680","exportType":"","entName":"","type":""}',
    }

    response = requests.post(
        'http://120.221.95.83:6080/declaration/epaViewListForJson',
        params=params,
        cookies=Common.getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    result_list = response.json()['data']
    print(result_list)
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    conn1 = pymysql.connect(**config.base_config_info)
    cursorTarget1 = conn1.cursor()
    for item in result_list:
        query = """select CREDIT_NO_TRUE from t_pub_company where COMPANY_NAME = %s limit 1"""
        cursorTarget1.execute(query, [item['a$entName']])
        # 获取所有记录列表
        results1 = cursorTarget1.fetchone()
        if results1 is None:
            continue
        data = {
            'ticketId': ticketId,
            'declarationId': item['a$id'],
        }
        response1 = requests.post(
            'http://120.221.95.83:6080/declarationGeneratedWaste/listForJson',
            cookies=Common.getCookie(session),
            headers=headers,
            data=data,
            verify=False,
        )
        x_list = response1.json()['data']
        for x in x_list:
            query = """select * from t_hsw_store_s_year_detail where CREDIT_NO=%s and COMPANY_NAME = %s
                                                                     and MONITOR_DATE = %s and HSW_CATE = %s
                                                                     and HSW_CATE_NAME = %s and HSW_CODE_NAME = %s
                                                                     and HSW_NAME = %s"""
            cursorTarget.execute(query, [results1[0],
                                         item['a$entName'],
                                         item['a$declarationTime'],
                                         x['wasteTypeCode'],
                                         x['generatedWasteName'],
                                         x['wasteCode'],
                                         x['generatedWasteName']
                                         ])
            # 获取所有记录列表
            results2 = cursorTarget.fetchall()
            if len(results2) == 0:
                sql = '''insert into t_hsw_store_s_year_detail (CREDIT_NO,
                                                            COMPANY_NAME,
                                                            MONITOR_DATE,
                                                            HSW_CATE,
                                                            HSW_CATE_NAME,
                                                            HSW_CODE_NAME,
                                                            HSW_NAME,
                                                            GENE_QTY,
                                                            TRANS_QTY,
                                                            CUR_STORE_QTY,
                                                            SELF_DISPOSE_QTY,
                                                            RECEIVE_QTY,
                                                            LAST_STORE_QTY,                         
                                                            SYS_CITY_CODE,
                                                            SYS_COUNTY_CODE
                                                           )values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000','370212000000')'''
                insert = cursorTarget.execute(sql,
                                              [results1[0],
                                               item['a$entName'],
                                               item['a$declarationTime'],
                                               x['wasteTypeCode'],
                                               x['generatedWasteName'],
                                               x['wasteCode'],
                                               x['generatedWasteName'],
                                               x['generation'],
                                               x['shiftOutSumQuantity'],
                                               x['storageSumQuantity'],
                                               x['disposalSumQuantity'],
                                               x['receiveSumQuantity'],
                                               x['capacityPastYear']
                                               ])
                print(insert)
                conn.commit()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='解析参数')
    parser.add_argument('--dateType', '-d', help='时间类型(1=小时；2=天；3=月；4=年)')
    args = parser.parse_args()
    if int(args.dateType) == 1:
        session = getSession()
        singleton_instance = Singleton()
        ticketId = singleton_instance.login(session)
        # 产生/经营月报
        getDangerMonth(ticketId, session)
        getProduceDangerMonth(ticketId, session)
        # 产生/经营月报细节
        getDangerMonthDetail(ticketId, session)
        getProduceDangerMonthDetail(ticketId, session)
    elif int(args.dateType) == 2:
        session = getSession()
        singleton_instance = Singleton()
        ticketId = singleton_instance.login(session)
        # 产生/经营年报
        getDangerYear(ticketId, session)
        getProduceDangerYear(ticketId, session)
        # 产生/经营年报细节
        getDangerYearDetail(ticketId, session)
        getProduceDangerYearDetail(ticketId, session)
    elif int(args.dateType) == 3:
        session = getSession()
        singleton_instance = Singleton()
        ticketId = singleton_instance.login(session)
        # 一般固废年报
        getSolidYear(ticketId, session)
        getProduceSolidYear(ticketId, session)
        # 一般固废年报细节
        getSolidYearDetail(ticketId, session)
        getProduceSolidYearDetail(ticketId, session)
