import argparse

import pymysql

import Common
from Kupono import Kupono, kupono_status, handle_status, trans_type, result_type, containerType
from Login import Singleton, getSession
from core import config


# 危固废_联单_基本信息抓取
# 省内,收集转移,医疗http://120.221.95.83:6080/solidwaste/transferManifest/listSpecialTransfer
# 跨省转入转出http://120.221.95.83:6080/solidwaste/transferManifest/epaList
# 一般固废http://120.221.95.83:6080/solidwaste/generalTransfer/listForApplyWithGeneral
# 数据库 dc_env_hsw.`t_hsw_kupono`

# 省内
def getProvince() -> object:
    # 1获取ticketId
    session = getSession()
    singleton_instance = Singleton()
    ticketId = singleton_instance.login(session)
    # 2获取联单数据
    params = {
        'ticketId': ticketId,
        'size': '50',
        'current': '1',
        'manifestNo': '',
        'transferPlanNo': '',
        'receiveEnterpriseName': '',
        'transEnterpriseName': '',
        'transportEnterpriseName': '',
        'busiStatusList': '',
        'startDate': '2023-01-01',
        'endDate': '',
        'exemptionType': '',
        'transBeginDate': '',
        'transEndDate': '',
        'receiveBeginDate': '',
        'receiveEndDate': '',
        'wasteCode': '',
        'wasteName': '',
        'dispositionTypeList': '',
        'actionType': 'WASTE_TRANSFER',
        'wasteTypeCode': '',
        'evaluateResult': '',
        'receiveLicenceNo': '',
        'isDangerousChemical': '',
        'transEnterpriseId': '',
        'entBusinessType': '',
        'transfer': '',
        'accept': '',
        'transportExemption': '',
        'dockingSource': '',
        'isRetroactive': '',
        'countryManifestNo': '',
    }
    response = Common.httpPostFromData("http://120.221.95.83:6080/solidwaste/transferManifest/listSpecialTransfer",
                                       params, session)
    cf_list = list(response.json()["data"])
    # 3连接数据库插入联单数据
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    for i in cf_list:
        item = Kupono()
        item.countryManifestNo = i['countryManifestNo']
        item.receiveEnterpriseName = i['receiveEnterpriseName']
        item.receiveAreaName = i['receiveAreaName']
        item.transEnterpriseName = i['transEnterpriseName']
        item.transAreaName = i['transAreaName']
        item.transportEnterpriseName = i['transportEnterpriseName']
        item.wasteNameStr = i['wasteNameStr']
        item.wasteType = i['wasteType']
        item.wasteCodeStr = i['wasteCodeStr']
        item.transferQuantityQuantitySum = i['transferQuantityQuantitySum']
        item.signQuantitySum = i['signQuantitySum']
        item.unit = i['unit']
        item.transDate = i['transDate']
        item.editedByName = i['editedByName']
        item.editedTime = i['editedTime']
        item.busiStatus = kupono_status.setdefault(i['busiStatus'], 0)
        item.progress = handle_status.setdefault(i['progress'], 0)
        # 4联单主表数据有些在详情里
        params1 = {
            'ticketId': ticketId,
            'id': i['id'],
        }
        response1 = Common.httpPostFromData(
            "http://120.221.95.83:6080/solidwaste/transferManifest/viewTransferManifest",
            params1, session)
        cf_list = response1.json()["obj"]['transferManifest']
        item.receiveContacts = cf_list['receiveContacts']
        item.transContacts = cf_list['transContacts']
        item.receiveContactsTel = cf_list['receiveContactsTel']
        item.transContactsTel = cf_list['transContactsTel']
        item.receiveLicenceNo = cf_list['receiveLicenceNo']
        item.transIinstCode = cf_list['transIinstCode']
        item.transAddress = cf_list['transAddress']
        item.receiveAddress = cf_list['receiveAddress']
        item.transportAddress = cf_list['transportAddress']
        item.transportQualification = cf_list['transportQualification']
        item.numberPlate = cf_list['numberPlate']
        item.transportContacts = cf_list['transportContacts']
        item.transportContactsTel = cf_list['transportContactsTel']
        item.transportCity = cf_list['transportCity']
        item.transportLine = cf_list['transportLine']
        item.transportMode = trans_type.setdefault(cf_list['transportMode'], 0)
        item.driverName = cf_list['driverName']
        item.driverPhone = cf_list['driverPhone']
        item.fileUrl = 'http://120.221.95.83:6080/exportPdfView?exportType=word&requestType=web&serviceName=WasteManifestDetailExportService&manifestId=' + \
                       i['id']
        if item.progress == 3:
            item.isHandleEnd = 1
        else:
            item.isHandleEnd = 0
        # 5不处理无联单号
        if item.countryManifestNo is None:
            continue
        if len(item.countryManifestNo) == 0:
            continue
        query = "SELECT * FROM t_hsw_kupono WHERE KUPONO_NO = %s"
        cursorTarget.execute(query, [i['countryManifestNo']])
        # 获取所有记录列表
        results = cursorTarget.fetchall()
        if len(results) == 0:
            sql = '''insert into t_hsw_kupono (
                            KUPONO_NO,
                            KUPONO_TYPE,
                            IS_YL,
                            RECEIVE_ORG,
                            RECEIVE_ORG_REGION,
                            OUT_ORG,
                            OUT_ORG_REGION,
                            RECEIVE_ORG_CONTACTS,
                            OUT_ORG_CONTACTS,
                            RECEIVE_ORG_TEL,
                            OUT_ORG_TEL,
                            RECEIVE_ORG_PERMIT,
                            OUT_ORG_CREDIT_NO,
                            RECEIVE_ORG_ADDRESS,
                            OUT_ORG_ADDRESS,
                            TRANS_ORG,
                            TRANS_REGION,
                            TRANS_CREDIT_NO,
                            TRANS_CAR_NO,
                            TRANS_CONTACTS,
                            TRANS_TEL,
                            TRANS_VIA_CITY,
                            TRANS_ROUTE,
                            TRANS_TYPE,
                            TRANS_DRIVER,
                            TRANS_DRIVER_TEL,
                            HSW_CATE_NAME,
                            HSW_CATE_TYPE,
                            HSW_CATE_CODE,
                            TRANS_AMOUNT,
                            REVEIVE_AMOUNT,
                            UNIT,
                            TRANS_TIME,
                            HANDLE_USER,
                            HANDLE_TIME,
                            KUPONO_STATUS,
                            HANDLE_STATUS,
                            IS_HANDLE_END,
                            FILE_URL,
                            SYS_CITY_CODE,
                            SYS_COUNTY_CODE
            ) values(%(countryManifestNo)s,
                    '1',
                    '0',
                    %(receiveEnterpriseName)s,
                    %(receiveAreaName)s,
                    %(transEnterpriseName)s,
                    %(transAreaName)s,
                    %(receiveContacts)s,
                    %(transContacts)s,
                    %(receiveContactsTel)s,
                    %(transContactsTel)s,
                    %(receiveLicenceNo)s,
                    %(transIinstCode)s,
                    %(receiveAddress)s,
                    %(transportAddress)s,
                    %(transportEnterpriseName)s,
                    %(transportAddress)s,
                    %(transportQualification)s,
                    %(numberPlate)s,
                    %(transportContacts)s,
                    %(transportContactsTel)s,
                    %(transportCity)s,
                    %(transportLine)s,
                    %(transportMode)s,
                    %(driverName)s,
                    %(driverPhone)s,
                    %(wasteNameStr)s,
                    %(wasteType)s,
                    %(wasteCodeStr)s,
                    %(transferQuantityQuantitySum)s,
                    %(signQuantitySum)s,
                    %(unit)s,
                    %(transDate)s,
                    %(editedByName)s,
                    %(editedTime)s,
                    %(busiStatus)s,
                    %(progress)s,
                    %(isHandleEnd)s,
                    %(fileUrl)s,
                    '370200000000',
                    '370212000000'
                    )
                    '''
            insert = cursorTarget.execute(sql, item.__dict__)
            print(insert)
            print('主表插入测试点')
            # 6转移动态与联单号关联
            params2 = {
                'ticketId': ticketId,
                'serviceId': i['id'],
                'enterpriseId': '',
            }
            response2 = Common.httpPostFromData("http://120.221.95.83:6080/solidwaste/systemLog/listInfo",
                                                params2, session)
            flow_list = response2.json()['data']
            for j in flow_list:
                query = "SELECT * FROM t_hsw_kupono_flow WHERE id = %s"
                cursorTarget.execute(query, [j['id']])
                # 获取所有记录列表
                results1 = cursorTarget.fetchall()
                if len(results1) == 0:
                    flow_sql = '''insert into t_hsw_kupono_flow (
                                                        ID,
                                                        KUPONO_ID,
                                                        HANDLE_TIME,
                                                        HANDLE_USER,
                                                        HANDLE_TYPE,
                                                        RESULT_TYPE,
                                                        REMARK,
                                                        SYS_CITY_CODE,
                                                        SYS_COUNTY_CODE
                                        ) values(%s,%s,%s,%s,%s,%s,%s,'370200000000',
                    '370212000000')'''
                    insert = cursorTarget.execute(flow_sql,
                                                  [j['id'], i['countryManifestNo'], j['operateTime'], j['operateBy'],
                                                   j['nodeCode'],
                                                   result_type.setdefault(j['result'], 1), j['remark']])
                    print(insert)
                    print('动态测试点')
            # 转移信息
            trans_list = response1.json()["obj"]['wasteList']
            for k in trans_list:
                # 查询转移批次的参数
                trans_sql = '''insert into t_hsw_kupono_trans ( KUPONO_NO, HSW_CATE_CODE, HSW_CATE_NAME, 
                TRANS_BATCH_NUM, TRANS_AMOUNT, DISPOSE_TYPE, DISPOSE_TYPE_CODE, SIGN_BATCH_NUM, SIGN_AMOUNT, HSW_ORG, 
                EME_DEVICE, NOTICE_MATTER, HSW_CHARACTER, HARMFUL_ELEMENT, HSW_FORM, CONTAIN_NUM, CONTAIN_TYPE, 
                CONTAIN_TYPE_NAME, SYS_CITY_CODE, SYS_COUNTY_CODE ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,'370200000000', '370212000000')'''
                insert = cursorTarget.execute(trans_sql,
                                              [i['countryManifestNo'],
                                               k['wasteCode'],
                                               k['wasteName'],
                                               k['parcelCnt'],
                                               k['transferQuantity'],
                                               k['dispositionTypeName'],
                                               k['dispositionType'],
                                               k['signParcelCnt'],
                                               k['signQuantity'],
                                               k['unit'],
                                               k['emergencyEquipment'],
                                               k['emergencyMeasure'],
                                               k['features'],
                                               k['harmfulComponents'],
                                               k['pattern'],
                                               k['containerNum'],
                                               k['containerType'],
                                               containerType.setdefault(k['containerType'], '') + '(' + k[
                                                   'containerMaterial'] + ')'
                                               ])
                print(insert)
                id = conn.insert_id()
                print('转移测试点')
                # 调接口查询批次转移信息
                params3 = {
                    'current': 1,
                    'generatedWasteId': k['generatedWasteId'],
                    'manifestId': k['manifestId'],
                    'manifestWasteId': k['id'],
                    'size': 10
                }
                response3 = Common.httpPostJsonData(
                    "http://120.221.95.83:6080/transferManifestWasteDetail/viewTransferManifestWasteDetail?ticketId=" + ticketId,
                    params3, session)
                trans_batch_list = response3.json()['data']

                for h in trans_batch_list:
                    trans_batch_sql = '''insert into t_hsw_kupono_trans_batch (
                                                                                            TRANS_ID,
                                                                                            BATCH_NO,
                                                                                            SCORE_FACTION,
                                                                                            HSW_CATE_NAME,
                                                                                            HSW_CATE_CODE,
                                                                                            TRANS_AMOUNT,
                                                                                            SIGN_AMOUNT,
                                                                                            UNIT,
                                                                                            SYS_CITY_CODE, 
                                                                                            SYS_COUNTY_CODE
                                                                            ) values(%s,%s,%s,%s,%s,%s,%s,%s,'370200000000',
                    '370212000000')'''
                    insert = cursorTarget.execute(trans_batch_sql,
                                                  [id,
                                                   h['batchCode'],
                                                   h['storageName'],
                                                   h['wasteName'],
                                                   h['wasteCode'],
                                                   h['transferQuantity'],
                                                   h['signQuantity'],
                                                   h['unit']
                                                   ])
                    print(insert)
                    print('批次测试点')
        else:
            sql_1 = "UPDATE t_hsw_kupono SET KUPONO_STATUS=%(busiStatus)s ,HANDLE_STATUS=%(progress)s,IS_HANDLE_END=%(isHandleEnd)s  WHERE KUPONO_NO=%(countryManifestNo)s"
            cursorTarget.execute(sql_1, item.__dict__)
            print()
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


# 跨省转入
def getInterProvince():
    # 1获取ticketId
    session = getSession()
    singleton_instance = Singleton()
    ticketId = singleton_instance.login(session)
    # 2获取联单数据
    params = {
        'ticketId': ticketId,
        'size': '10',
        'current': '1',
        'manifestNo': '',
        'receiveEnterpriseName': '',
        'transEnterpriseName': '',
        'busiStatus': '',
        'transBeginDate': '2023-01-01',
        'transEndDate': '',
        'receiveBeginDate': '',
        'receiveEndDate': '',
        'dispositionType': '',
        'manifestType': 'KS_TURN_IN',
        'transferPlanNo': '',
        'isDocking': '1',
        'actionType': 'KS_TURN_IN',
        'wasteTypeCode': '',
        'wasteCode': ''
    }
    response = Common.httpPostFromData("http://120.221.95.83:6080/solidwaste/transferManifest/epaList",
                                       params, session)
    # 拉不到数据不知道内部结构
    cf_list = list(response.json()["data"])


# 跨省转出
def getOuterProvince():
    # 1获取ticketId
    session = getSession()
    singleton_instance = Singleton()
    ticketId = singleton_instance.login(session)
    # 2获取联单数据
    params = {
        'ticketId': ticketId,
        'size': 10,
        'current': 1,
        'manifestNo': '',
        'receiveEnterpriseName': '',
        'transEnterpriseName': '',
        'transportEnterpriseName': '',
        'busiStatus': '',
        'startDate': '2023-01-01',
        'endDate': '',
        'transBeginDate': '',
        'transEndDate': '',
        'receiveBeginDate': '',
        'receiveEndDate': '',
        'dispositionType': '',
        'attachmentFlag': '',
        'manifestType': 'KS_TURN_OUT',
        'wasteCode': '',
        'wasteName': '',
        'wasteTypeCode': '',
        'actionType': 'KS_TURN_OUT',
        'exemptionType': '',
    }
    response = Common.httpPostFromData("http://120.221.95.83:6080/solidwaste/transferManifest/epaList",
                                       params, session)
    # 拉不到数据不知道内部结构
    cf_list = list(response.json()["data"])


# 收集转移
def getCollect():
    # 1获取ticketId
    session = getSession()
    singleton_instance = Singleton()
    ticketId = singleton_instance.login(session)
    # 2获取联单数据
    params = {
        'ticketId': ticketId,
        'size': '50',
        'current': '1',
        'manifestNo': '',
        'transferPlanNo': '',
        'receiveEnterpriseName': '',
        'transEnterpriseName': '',
        'transportEnterpriseName': '',
        'busiStatusList': '',
        'startDate': '2023-01-01',
        'endDate': '',
        'exemptionType': '',
        'transBeginDate': '',
        'transEndDate': '',
        'receiveBeginDate': '',
        'receiveEndDate': '',
        'wasteCode': '',
        'wasteName': '',
        'dispositionTypeList': '',
        'actionType': 'COLLECT_TRANSFER',
        'wasteTypeCode': '',
        'evaluateResult': '',
        'receiveLicenceNo': '',
        'isDangerousChemical': '',
        'transEnterpriseId': '',
        'entBusinessType': '',
        'transfer': '',
        'accept': '',
        'transportExemption': '',
        'dockingSource': '',
        'isRetroactive': '',
        'countryManifestNo': '',
    }
    response = Common.httpPostFromData("http://120.221.95.83:6080/solidwaste/transferManifest/listSpecialTransfer",
                                       params, session)
    cf_list = list(response.json()["data"])
    # 3连接数据库插入联单数据
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    for i in cf_list:
        item = Kupono()
        item.countryManifestNo = i['countryManifestNo']
        item.receiveEnterpriseName = i['receiveEnterpriseName']
        item.receiveAreaName = i['receiveAreaName']
        item.transEnterpriseName = i['transEnterpriseName']
        item.transAreaName = i['transAreaName']
        item.transportEnterpriseName = i['transportEnterpriseName']
        item.wasteNameStr = i['wasteNameStr']
        item.wasteType = i['wasteType']
        item.wasteCodeStr = i['wasteCodeStr']
        item.transferQuantityQuantitySum = i['transferQuantityQuantitySum']
        item.signQuantitySum = i['signQuantitySum']
        item.unit = i['unit']
        item.transDate = i['transDate']
        item.editedByName = i['editedByName']
        item.editedTime = i['editedTime']
        item.busiStatus = kupono_status.setdefault(i['busiStatus'], 0)
        item.progress = handle_status.setdefault(i['progress'], 0)
        # 4联单主表数据有些在详情里
        params1 = {
            'ticketId': ticketId,
            'id': i['id'],
        }
        response1 = Common.httpPostFromData(
            "http://120.221.95.83:6080/solidwaste/transferManifest/viewTransferManifest",
            params1, session)
        cf_list = response1.json()["obj"]['transferManifest']
        item.receiveContacts = cf_list['receiveContacts']
        item.transContacts = cf_list['transContacts']
        item.receiveContactsTel = cf_list['receiveContactsTel']
        item.transContactsTel = cf_list['transContactsTel']
        item.receiveLicenceNo = cf_list['receiveLicenceNo']
        item.transIinstCode = cf_list['transIinstCode']
        item.transAddress = cf_list['transAddress']
        item.receiveAddress = cf_list['receiveAddress']
        item.transportAddress = cf_list['transportAddress']
        item.transportQualification = cf_list['transportQualification']
        item.numberPlate = cf_list['numberPlate']
        item.transportContacts = cf_list['transportContacts']
        item.transportContactsTel = cf_list['transportContactsTel']
        item.transportCity = cf_list['transportCity']
        item.transportLine = cf_list['transportLine']
        item.transportMode = trans_type.setdefault(cf_list['transportMode'], 0)
        item.driverName = cf_list['driverName']
        item.driverPhone = cf_list['driverPhone']
        item.fileUrl = 'http://120.221.95.83:6080/exportPdfView?exportType=word&requestType=web&serviceName=WasteManifestDetailExportService&manifestId=' + \
                       i['id']
        if item.progress == 3:
            item.isHandleEnd = 1
        else:
            item.isHandleEnd = 0
        # 5不处理无联单号
        if len(item.countryManifestNo) == 0:
            continue
        query = "SELECT * FROM t_hsw_kupono WHERE KUPONO_NO = %s"
        cursorTarget.execute(query, [i['countryManifestNo']])
        # 获取所有记录列表
        results = cursorTarget.fetchall()
        if len(results) == 0:
            sql = '''insert into t_hsw_kupono (
                                KUPONO_NO,
                                KUPONO_TYPE,
                                IS_YL,
                                RECEIVE_ORG,
                                RECEIVE_ORG_REGION,
                                OUT_ORG,
                                OUT_ORG_REGION,
                                RECEIVE_ORG_CONTACTS,
                                OUT_ORG_CONTACTS,
                                RECEIVE_ORG_TEL,
                                OUT_ORG_TEL,
                                RECEIVE_ORG_PERMIT,
                                OUT_ORG_CREDIT_NO,
                                RECEIVE_ORG_ADDRESS,
                                OUT_ORG_ADDRESS,
                                TRANS_ORG,
                                TRANS_REGION,
                                TRANS_CREDIT_NO,
                                TRANS_CAR_NO,
                                TRANS_CONTACTS,
                                TRANS_TEL,
                                TRANS_VIA_CITY,
                                TRANS_ROUTE,
                                TRANS_TYPE,
                                TRANS_DRIVER,
                                TRANS_DRIVER_TEL,
                                HSW_CATE_NAME,
                                HSW_CATE_TYPE,
                                HSW_CATE_CODE,
                                TRANS_AMOUNT,
                                REVEIVE_AMOUNT,
                                UNIT,
                                TRANS_TIME,
                                HANDLE_USER,
                                HANDLE_TIME,
                                KUPONO_STATUS,
                                HANDLE_STATUS,
                                IS_HANDLE_END,
                                FILE_URL,
                                SYS_CITY_CODE,
                                SYS_COUNTY_CODE
                ) values(%(countryManifestNo)s,
                        '4',
                        '0',
                        %(receiveEnterpriseName)s,
                        %(receiveAreaName)s,
                        %(transEnterpriseName)s,
                        %(transAreaName)s,
                        %(receiveContacts)s,
                        %(transContacts)s,
                        %(receiveContactsTel)s,
                        %(transContactsTel)s,
                        %(receiveLicenceNo)s,
                        %(transIinstCode)s,
                        %(receiveAddress)s,
                        %(transportAddress)s,
                        %(transportEnterpriseName)s,
                        %(transportAddress)s,
                        %(transportQualification)s,
                        %(numberPlate)s,
                        %(transportContacts)s,
                        %(transportContactsTel)s,
                        %(transportCity)s,
                        %(transportLine)s,
                        %(transportMode)s,
                        %(driverName)s,
                        %(driverPhone)s,
                        %(wasteNameStr)s,
                        %(wasteType)s,
                        %(wasteCodeStr)s,
                        %(transferQuantityQuantitySum)s,
                        %(signQuantitySum)s,
                        %(unit)s,
                        %(transDate)s,
                        %(editedByName)s,
                        %(editedTime)s,
                        %(busiStatus)s,
                        %(progress)s,
                        %(isHandleEnd)s,
                        %(fileUrl)s,
                        '370200000000',
                        '370212000000'
                        )
                        '''
            insert = cursorTarget.execute(sql, item.__dict__)
            print(insert)
            print('主表插入测试点')
            # 6转移动态与联单号关联
            params2 = {
                'ticketId': ticketId,
                'serviceId': i['id'],
                'enterpriseId': '',
            }
            response2 = Common.httpPostFromData("http://120.221.95.83:6080/solidwaste/systemLog/listInfo",
                                                params2, session)
            flow_list = response2.json()['data']
            for j in flow_list:
                query = "SELECT * FROM t_hsw_kupono_flow WHERE id = %s"
                cursorTarget.execute(query, [j['id']])
                # 获取所有记录列表
                results1 = cursorTarget.fetchall()
                if len(results1) == 0:
                    flow_sql = '''insert into t_hsw_kupono_flow (
                                                            ID,
                                                            KUPONO_ID,
                                                            HANDLE_TIME,
                                                            HANDLE_USER,
                                                            HANDLE_TYPE,
                                                            RESULT_TYPE,
                                                            REMARK,
                                                             SYS_CITY_CODE,
                                SYS_COUNTY_CODE
                                            ) values(%s,%s,%s,%s,%s,%s,%s,'370200000000',
                        '370212000000')'''
                    insert = cursorTarget.execute(flow_sql,
                                                  [j['id'], i['countryManifestNo'], j['operateTime'], j['operateBy'],
                                                   j['nodeCode'],
                                                   result_type.setdefault(j['result'], 1), j['remark']])
                    print(insert)
                    print('动态测试点')
            # 转移信息
            trans_list = response1.json()["obj"]['wasteList']
            for k in trans_list:
                # 查询转移批次的参数
                trans_sql = '''insert into t_hsw_kupono_trans (                                                
                                                                            KUPONO_NO,
                                                                            HSW_CATE_CODE,
                                                                            HSW_CATE_NAME,
                                                                            TRANS_BATCH_NUM,
                                                                            TRANS_AMOUNT,
                                                                            DISPOSE_TYPE,
                                                                            DISPOSE_TYPE_CODE,
                                                                            SIGN_BATCH_NUM,
                                                                            SIGN_AMOUNT,
                                                                            HSW_ORG,
                                                                            EME_DEVICE,
                                                                            NOTICE_MATTER,
                                                                            HSW_CHARACTER,
                                                                            HARMFUL_ELEMENT,
                                                                            HSW_FORM,
                                                                            CONTAIN_NUM,
                                                                            CONTAIN_TYPE,
                                                                            CONTAIN_TYPE_NAME,
                                                                            SYS_CITY_CODE,
                                SYS_COUNTY_CODE
                                                            ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000',
                        '370212000000')'''
                insert = cursorTarget.execute(trans_sql,
                                              [i['countryManifestNo'],
                                               k['wasteCode'],
                                               k['wasteName'],
                                               k['parcelCnt'],
                                               k['transferQuantity'],
                                               k['dispositionTypeName'],
                                               k['dispositionType'],
                                               k['signParcelCnt'],
                                               k['signQuantity'],
                                               k['unit'],
                                               k['emergencyEquipment'],
                                               k['emergencyMeasure'],
                                               k['features'],
                                               k['harmfulComponents'],
                                               k['pattern'],
                                               k['containerNum'],
                                               k['containerType'],
                                               containerType.setdefault(k['containerType'], '') + '(' + k[
                                                   'containerMaterial'] + ')'
                                               ])
                print(insert)
                id = conn.insert_id()
                print('转移测试点')
                # 调接口查询批次转移信息
                params3 = {
                    'current': 1,
                    'generatedWasteId': k['generatedWasteId'],
                    'manifestId': k['manifestId'],
                    'manifestWasteId': k['id'],
                    'size': 10
                }
                response3 = Common.httpPostJsonData(
                    "http://120.221.95.83:6080/transferManifestWasteDetail/viewTransferManifestWasteDetail?ticketId=" + ticketId,
                    params3, session)
                trans_batch_list = response3.json()['data']

                for h in trans_batch_list:
                    trans_batch_sql = '''insert into t_hsw_kupono_trans_batch (
                                                                                                TRANS_ID,
                                                                                                BATCH_NO,
                                                                                                SCORE_FACTION,
                                                                                                HSW_CATE_NAME,
                                                                                                HSW_CATE_CODE,
                                                                                                TRANS_AMOUNT,
                                                                                                SIGN_AMOUNT,
                                                                                                UNIT,
                                                                                                SYS_CITY_CODE,
                                SYS_COUNTY_CODE
                                                                                ) values(%s,%s,%s,%s,%s,%s,%s,%s,'370200000000',
                        '370212000000')'''
                    insert = cursorTarget.execute(trans_batch_sql,
                                                  [id,
                                                   h['batchCode'],
                                                   h['storageName'],
                                                   h['wasteName'],
                                                   h['wasteCode'],
                                                   h['transferQuantity'],
                                                   h['signQuantity'],
                                                   h['unit']
                                                   ])
                    print(insert)
                    print('批次测试点')
        else:
            sql_1 = "UPDATE t_hsw_kupono SET KUPONO_STATUS=%(busiStatus)s ,HANDLE_STATUS=%(progress)s,IS_HANDLE_END=%(isHandleEnd)s  WHERE KUPONO_NO=%(countryManifestNo)s"
            cursorTarget.execute(sql_1, item.__dict__)
            print()
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


# 医疗废物
def getMedical():
    # 1获取ticketId
    session = getSession()
    singleton_instance = Singleton()
    ticketId = singleton_instance.login(session)
    # 2获取联单数据
    params = {
        'ticketId': ticketId,
        'size': '50',
        'current': '1',
        'manifestNo': '',
        'transferPlanNo': '',
        'receiveEnterpriseName': '',
        'transEnterpriseName': '',
        'transportEnterpriseName': '',
        'busiStatusList': '',
        'startDate': '2023-01-01',
        'endDate': '',
        'exemptionType': '',
        'transBeginDate': '',
        'transEndDate': '',
        'receiveBeginDate': '',
        'receiveEndDate': '',
        'wasteCode': '',
        'wasteName': '',
        'dispositionTypeList': '',
        'actionType': 'WASTE_TRANSFER',
        'wasteTypeCode': '',
        'evaluateResult': '',
        'receiveLicenceNo': '',
        'isDangerousChemical': '',
        'transEnterpriseId': '',
        'entBusinessType': 'YL',
        'transfer': '',
        'accept': '',
        'transportExemption': '',
        'dockingSource': '',
        'isRetroactive': '',
        'countryManifestNo': '',
    }
    response = Common.httpPostFromData("http://120.221.95.83:6080/solidwaste/transferManifest/listSpecialTransfer",
                                       params, session)
    cf_list = list(response.json()["data"])
    # 3连接数据库插入联单数据
    conn = pymysql.connect(**config.hsw_config_info)
    cursorTarget = conn.cursor()
    for i in cf_list:
        item = Kupono()
        item.countryManifestNo = i['countryManifestNo']
        item.receiveEnterpriseName = i['receiveEnterpriseName']
        item.receiveAreaName = i['receiveAreaName']
        item.transEnterpriseName = i['transEnterpriseName']
        item.transAreaName = i['transAreaName']
        item.transportEnterpriseName = i['transportEnterpriseName']
        item.wasteNameStr = i['wasteNameStr']
        item.wasteType = i['wasteType']
        item.wasteCodeStr = i['wasteCodeStr']
        item.transferQuantityQuantitySum = i['transferQuantityQuantitySum']
        item.signQuantitySum = i['signQuantitySum']
        item.unit = i['unit']
        item.transDate = i['transDate']
        item.editedByName = i['editedByName']
        item.editedTime = i['editedTime']
        item.busiStatus = kupono_status.setdefault(i['busiStatus'], 0)
        item.progress = handle_status.setdefault(i['progress'], 0)
        # 4联单主表数据有些在详情里
        params1 = {
            'ticketId': ticketId,
            'id': i['id'],
        }
        response1 = Common.httpPostFromData(
            "http://120.221.95.83:6080/solidwaste/transferManifest/viewTransferManifest",
            params1, session)
        cf_list = response1.json()["obj"]['transferManifest']
        item.receiveContacts = cf_list['receiveContacts']
        item.transContacts = cf_list['transContacts']
        item.receiveContactsTel = cf_list['receiveContactsTel']
        item.transContactsTel = cf_list['transContactsTel']
        item.receiveLicenceNo = cf_list['receiveLicenceNo']
        item.transIinstCode = cf_list['transIinstCode']
        item.transAddress = cf_list['transAddress']
        item.receiveAddress = cf_list['receiveAddress']
        item.transportAddress = cf_list['transportAddress']
        item.transportQualification = cf_list['transportQualification']
        item.numberPlate = cf_list['numberPlate']
        item.transportContacts = cf_list['transportContacts']
        item.transportContactsTel = cf_list['transportContactsTel']
        item.transportCity = cf_list['transportCity']
        item.transportLine = cf_list['transportLine']
        item.transportMode = trans_type.setdefault(cf_list['transportMode'], 0)
        item.driverName = cf_list['driverName']
        item.driverPhone = cf_list['driverPhone']
        item.fileUrl = 'http://120.221.95.83:6080/exportPdfView?exportType=word&requestType=web&serviceName=WasteManifestDetailExportService&manifestId=' + \
                       i['id']
        if item.progress == 3:
            item.isHandleEnd = 1
        else:
            item.isHandleEnd = 0
        # 5不处理无联单号
        if item.countryManifestNo is None:
            continue
        if len(item.countryManifestNo) == 0:
            continue
        query = "SELECT * FROM t_hsw_kupono WHERE KUPONO_NO = %s"
        cursorTarget.execute(query, [i['countryManifestNo']])
        # 获取所有记录列表
        results = cursorTarget.fetchall()
        if len(results) == 0:
            sql = '''insert into t_hsw_kupono (
                                KUPONO_NO,
                                KUPONO_TYPE,
                                IS_YL,
                                RECEIVE_ORG,
                                RECEIVE_ORG_REGION,
                                OUT_ORG,
                                OUT_ORG_REGION,
                                RECEIVE_ORG_CONTACTS,
                                OUT_ORG_CONTACTS,
                                RECEIVE_ORG_TEL,
                                OUT_ORG_TEL,
                                RECEIVE_ORG_PERMIT,
                                OUT_ORG_CREDIT_NO,
                                RECEIVE_ORG_ADDRESS,
                                OUT_ORG_ADDRESS,
                                TRANS_ORG,
                                TRANS_REGION,
                                TRANS_CREDIT_NO,
                                TRANS_CAR_NO,
                                TRANS_CONTACTS,
                                TRANS_TEL,
                                TRANS_VIA_CITY,
                                TRANS_ROUTE,
                                TRANS_TYPE,
                                TRANS_DRIVER,
                                TRANS_DRIVER_TEL,
                                HSW_CATE_NAME,
                                HSW_CATE_TYPE,
                                HSW_CATE_CODE,
                                TRANS_AMOUNT,
                                REVEIVE_AMOUNT,
                                UNIT,
                                TRANS_TIME,
                                HANDLE_USER,
                                HANDLE_TIME,
                                KUPONO_STATUS,
                                HANDLE_STATUS,
                                IS_HANDLE_END,
                                FILE_URL,
                                SYS_CITY_CODE,
                                SYS_COUNTY_CODE
                ) values(%(countryManifestNo)s,
                        '1',
                        '1',
                        %(receiveEnterpriseName)s,
                        %(receiveAreaName)s,
                        %(transEnterpriseName)s,
                        %(transAreaName)s,
                        %(receiveContacts)s,
                        %(transContacts)s,
                        %(receiveContactsTel)s,
                        %(transContactsTel)s,
                        %(receiveLicenceNo)s,
                        %(transIinstCode)s,
                        %(receiveAddress)s,
                        %(transportAddress)s,
                        %(transportEnterpriseName)s,
                        %(transportAddress)s,
                        %(transportQualification)s,
                        %(numberPlate)s,
                        %(transportContacts)s,
                        %(transportContactsTel)s,
                        %(transportCity)s,
                        %(transportLine)s,
                        %(transportMode)s,
                        %(driverName)s,
                        %(driverPhone)s,
                        %(wasteNameStr)s,
                        %(wasteType)s,
                        %(wasteCodeStr)s,
                        %(transferQuantityQuantitySum)s,
                        %(signQuantitySum)s,
                        %(unit)s,
                        %(transDate)s,
                        %(editedByName)s,
                        %(editedTime)s,
                        %(busiStatus)s,
                        %(progress)s,
                        %(isHandleEnd)s,
                        %(fileUrl)s,
                        '370200000000',
                        '370212000000'
                        )
                        '''
            insert = cursorTarget.execute(sql, item.__dict__)
            print(insert)
            print('主表插入测试点')
            # 6转移动态与联单号关联
            params2 = {
                'ticketId': ticketId,
                'serviceId': i['id'],
                'enterpriseId': '',
            }
            response2 = Common.httpPostFromData("http://120.221.95.83:6080/solidwaste/systemLog/listInfo",
                                                params2, session)
            flow_list = response2.json()['data']
            for j in flow_list:
                query = "SELECT * FROM t_hsw_kupono_flow WHERE id = %s"
                cursorTarget.execute(query, [j['id']])
                # 获取所有记录列表
                results1 = cursorTarget.fetchall()
                if len(results1) == 0:
                    flow_sql = '''insert into t_hsw_kupono_flow (
                                                            ID,
                                                            KUPONO_ID,
                                                            HANDLE_TIME,
                                                            HANDLE_USER,
                                                            HANDLE_TYPE,
                                                            RESULT_TYPE,
                                                            REMARK,
                                                            SYS_CITY_CODE,
                                SYS_COUNTY_CODE
                                            ) values(%s,%s,%s,%s,%s,%s,%s,'370200000000',
                        '370212000000')'''
                    insert = cursorTarget.execute(flow_sql,
                                                  [j['id'], i['countryManifestNo'], j['operateTime'], j['operateBy'],
                                                   j['nodeCode'],
                                                   result_type.setdefault(j['result'], 1), j['remark']])
                    print(insert)
                    print('动态测试点')
            # 转移信息
            trans_list = response1.json()["obj"]['wasteList']
            for k in trans_list:
                # 查询转移批次的参数
                trans_sql = '''insert into t_hsw_kupono_trans (                                                
                                                                            KUPONO_NO,
                                                                            HSW_CATE_CODE,
                                                                            HSW_CATE_NAME,
                                                                            TRANS_BATCH_NUM,
                                                                            TRANS_AMOUNT,
                                                                            DISPOSE_TYPE,
                                                                            DISPOSE_TYPE_CODE,
                                                                            SIGN_BATCH_NUM,
                                                                            SIGN_AMOUNT,
                                                                            HSW_ORG,
                                                                            EME_DEVICE,
                                                                            NOTICE_MATTER,
                                                                            HSW_CHARACTER,
                                                                            HARMFUL_ELEMENT,
                                                                            HSW_FORM,
                                                                            CONTAIN_NUM,
                                                                            CONTAIN_TYPE,
                                                                            CONTAIN_TYPE_NAME,
                                                                            SYS_CITY_CODE,
                                SYS_COUNTY_CODE
                                                            ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'370200000000',
                        '370212000000')'''
                insert = cursorTarget.execute(trans_sql,
                                              [i['countryManifestNo'],
                                               k['wasteCode'],
                                               k['wasteName'],
                                               k['parcelCnt'],
                                               k['transferQuantity'],
                                               k['dispositionTypeName'],
                                               k['dispositionType'],
                                               k['signParcelCnt'],
                                               k['signQuantity'],
                                               k['unit'],
                                               k['emergencyEquipment'],
                                               k['emergencyMeasure'],
                                               k['features'],
                                               k['harmfulComponents'],
                                               k['pattern'],
                                               k['containerNum'],
                                               k['containerType'],
                                               containerType.setdefault(k['containerType'], '') + '(' + k[
                                                   'containerMaterial'] + ')'
                                               ])
                print(insert)
                id = conn.insert_id()
                print('转移测试点')
                # 调接口查询批次转移信息
                params3 = {
                    'current': 1,
                    'generatedWasteId': k['generatedWasteId'],
                    'manifestId': k['manifestId'],
                    'manifestWasteId': k['id'],
                    'size': 10
                }
                response3 = Common.httpPostJsonData(
                    "http://120.221.95.83:6080/transferManifestWasteDetail/viewTransferManifestWasteDetail?ticketId=" + ticketId,
                    params3, session)
                trans_batch_list = response3.json()['data']

                for h in trans_batch_list:
                    trans_batch_sql = '''insert into t_hsw_kupono_trans_batch (
                                                                                                TRANS_ID,
                                                                                                BATCH_NO,
                                                                                                SCORE_FACTION,
                                                                                                HSW_CATE_NAME,
                                                                                                HSW_CATE_CODE,
                                                                                                TRANS_AMOUNT,
                                                                                                SIGN_AMOUNT,
                                                                                                UNIT,
                                                                                                 SYS_CITY_CODE,
                                SYS_COUNTY_CODE
                                                                                ) values(%s,%s,%s,%s,%s,%s,%s,%s,'370200000000',
                        '370212000000')'''
                    insert = cursorTarget.execute(trans_batch_sql,
                                                  [id,
                                                   h['batchCode'],
                                                   h['storageName'],
                                                   h['wasteName'],
                                                   h['wasteCode'],
                                                   h['transferQuantity'],
                                                   h['signQuantity'],
                                                   h['unit']
                                                   ])
                    print(insert)
                    print('批次测试点')
        else:
            sql_1 = "UPDATE t_hsw_kupono SET KUPONO_STATUS=%(busiStatus)s ,HANDLE_STATUS=%(progress)s,IS_HANDLE_END=%(isHandleEnd)s  WHERE KUPONO_NO=%(countryManifestNo)s"
            cursorTarget.execute(sql_1, item.__dict__)
            print()
    try:
        conn.commit()
    except:
        conn.rollback()
    cursorTarget.close()
    # 关闭连接
    conn.close()
    print("成功")


# 一般固废物
def getSolid():
    # 1获取ticketId
    session = getSession()
    singleton_instance = Singleton()
    ticketId = singleton_instance.login(session)
    # 2获取联单数据
    params = {
        'ticketId': ticketId,
        'size': 10,
        'current': 1,
        'transferNo': '',
        'receiveEnterpriseName': '',
        'entName': '',
        'busiStatus': '',
        'transBeginDate': '2023-07-01',
        'transEndDate': '',
        'receiveBeginDate': '',
        'receiveEndDate': '',
        'dispositionType': '',
        'type': '',
        'manifestType': 'GENERAL_MANIFEST',
    }
    response = Common.httpPostFromData("http://120.221.95.83:6080/solidwaste/generalTransfer/listForApplyWithGeneral",
                                       params, session)
    # 拉不到数据不知道内部结构
    cf_list = list(response.json()["data"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='解析参数')
    parser.add_argument('--dateType', '-d', help='时间类型(1=小时；2=天；3=月；4=年)')
    args = parser.parse_args()
    if int(args.dateType) == 1:
        getProvince()
    elif int(args.dateType) == 2:
        getCollect()
    elif int(args.dateType) == 3:
        getMedical()
