import json
import time
import requests
import pymysql
import hashlib
import datetime

from cop.configs import headers, \
    loginData, loginUrl, detailParams, detailUrl, sessionUrl, iconUrl, \
    compDetailUrl, baseHeaders, queryTechList, queryElectricityDataUrl

# 生产环境
# connect = pymysql.connect(host='10.35.0.147',
#                           port=13306,
#                           user='root',
#                           password='Xizheng123!',
#                           db='pd_env_spider',
#                           charset='utf8')
# 测试环境
connect = pymysql.connect(host='192.168.110.157',
                          port=3306,
                          user='root',
                          password='Xizheng123!',
                          db='dc_env_cem',
                          charset='utf8')
cur = connect.cursor()


def checkData(data):
    if data == '' or data is None or data == "":
        return [0.00]
    else:
        return data


# 27 有功功率； 33 有功电能； 31 总有功电能 ；47 总无功电能 ；48总无功功率；39正向无功电能；37正向有功电能；21 a向电流；22 b向电流 ；23 c向电流；24 a向电压；
# 25 b相电压；26 c向电压；44c向功率因数 45 b向功率因数 46 a相功率因数 32总功率因数；43 a向无功功率；42 b向无功功率 ；41 c向无功功率；28 a向有功功率；29 b向有功功率 30 c向有功功率
# 40 反向无功电能 38 反向有功电能 34修正电能
itemcode = [33, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
# 对应网站的参数与数据库字段对照
itemcodename = {20: "ACTIVE_POWER", 21: "A_DIRECTION_CURRENT", 22: "B_DIRECTION_CURRENT", 23: "C_DIRECTION_CURRENT",
                24: "A_DIRECTION_VOLTAGE", 25: "B_DIRECTION_VOLTAGE", 26: "C_DIRECTION_VOLTAGE"
    , 27: "ACTIVE_POWER", 28: "A_DIRECTION_ACTIVE_POWER", 29: "B_DIRECTION_ACTIVE_POWER",
                30: "C_DIRECTION_ACTIVE_POWER", 31: "TOTAL_ACTIVE_ELECTRIC_ENERGY", 34: "CORRECTED_ELECTRIC_ENERGY",
                37: "POSITIVE_ACTIVE_ELECTRIC_ENERGY", 39: "POSITIVE_REACTIVE_ELECTRIC_ENERGY",
                40: "REVERSE_REACTIVE_ELECTRIC_ENERGY", 41: "C_DIRECTION_REACTIVE_POWER",
                42: "B_DIRECTION_REACTIVE_POWER", 43: "A_DIRECTION_REACTIVE_POWER", 44: "C_DIRECTION_POWER_FACTOR",
                45: "B_DIRECTION_POWER_FACTOR", 46: "A_DIRECTION_POWER_FACTOR",
                47: "TOTAL_REACTIVE_ELECTRIC_ENERGY", 48: "TOTAL_REACTIVE_POWER", 32: "TOTAL_POWER_FACTOR"}


def requestData(start):
    response = requests.get(sessionUrl, headers=baseHeaders, verify=False)
    sessionId = response.cookies.get("jeesite.session.id")
    cookies = {
        'jeesite.session.id': sessionId,
    }
    response = requests.post(loginUrl, cookies=cookies, headers=headers, data=loginData,
                             verify=False)
    response = requests.get(iconUrl, cookies=cookies, headers=headers, verify=False)
    cookies = {
        'jeesite.session.id': sessionId,
        'JSESSIONID': response.cookies.get("JSESSIONID"),
    }
    selectyCompSql = "select CEM_CODE,FK_PROD_LINE_ID,CREDIT_NO from t_cem_prod_line" \
                     " group by CEM_CODE,FK_PROD_LINE_ID,CREDIT_NO"
    try:
        # 执行SQL语句
        cur.execute(selectyCompSql)

        # 获取所有记录列表,以元组来存储
        results = cur.fetchall()
        # 遍历元组存值 每项为一个企业
        for row in results:
            company_id = row[0]
            production_line_id = row[1]
            CREDIT_NO = row[2]
            # times = time.localtime(time.time())
            end = (start + datetime.timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")

            # end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            itemdict = dict()
            # 遍历数据 每项为一个企业中的一个请求
            for i in itemcode:
                electricityData = {
                    'c0902id': company_id,
                    'techId': production_line_id,
                    'startTime': start.strftime("%Y-%m-%d %H:%M:%S"),
                    # 'endTime': endtime.strftime("%Y-%m-%d %H:%M:%S"),
                    'endTime': end,
                    # 'startTime': "2023-06-02 00:00:00",
                    # 'endTime':  "2023-06-04 23:59:59",
                    'itemCode': i,
                }
                queryElectricityGetData = requests.post(queryElectricityDataUrl, cookies=cookies,
                                                        headers=headers, data=electricityData, verify=False)
                queryElectricityData = json.loads(queryElectricityGetData.text)
                itemdict[i] = queryElectricityData
                print("请求到" + str(i))
            # electricityData = {
            #     'c0902id': company_id,
            #     'techId': production_line_id,
            #     'startTime': start,
            #     'endTime': endtime.strftime("%Y-%m-%d %H:%M:%S"),
            #     # 'startTime': "2022-09-13 12:30:00",
            #     # 'endTime':  "2022-09-13 12:45:01",
            #     'itemCode': '33',
            # }
            # queryElectricityGetData = requests.post(queryElectricityDataUrl, cookies=cookies,
            #                                         headers=headers, data=electricityData, verify=False)
            count = 0

            for key in itemdict:
                # 新增程序，先新增一条，随后循环更新此条数据
                if key == 33:
                    # 企业用电新增
                    if itemdict[key]['scList'] is not None:
                        for elecScList in range(len(itemdict[key]['scList'])):
                            # 数据列表
                            YDL = itemdict[key]['scList'][elecScList]['YDL']
                            for details in range(len(YDL)):
                                YDLs = YDL[details]
                                # 工艺线名称
                                DEVICENAME = itemdict[key]['scList'][elecScList]['DEVICENAME']
                                insert_detail_sql = "insert into t_cem_monitor_realtime (DEVICE_ID,CREDIT_NO,PROD_LINE_ID," \
                                                    "FACILITY_ID,DEVICE_NAME,MONITOR_TIME," \
                                                    "TOTAL_PCC,SYS_CITY_CODE,SYS_COUNTY_CODE) " \
                                                    "values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                insert_detail_param = (
                                    hashlib.md5(
                                        str((DEVICENAME) + str(hashlib.md5(
                                            (production_line_id + "sc").encode(encoding="utf-8")).hexdigest()) +
                                            str(production_line_id) + str(company_id)).encode(
                                            encoding="utf-8")).hexdigest(),
                                    CREDIT_NO,
                                    production_line_id,
                                    hashlib.md5(
                                        ((production_line_id + "sc").encode(encoding='utf-8'))).hexdigest(),
                                    DEVICENAME,
                                    itemdict[key]['category'][details],
                                    checkData(YDLs),
                                    '370200000000',
                                    '370212000000'

                                )

                                cur.execute(insert_detail_sql, insert_detail_param)
                        # 企业治污新增
                        if itemdict[key]['zwList'] is not None:
                            for elecScList in range(len(itemdict[key]['zwList'])):
                                # 数据列表
                                YDL = itemdict[key]['zwList'][elecScList]['YDL']
                                for details in range(len(YDL)):
                                    YDLs = YDL[details]
                                    # 工艺线名称
                                    DEVICENAME = itemdict[key]['zwList'][elecScList]['DEVICENAME']
                                    insert_detail_sql = "insert into t_cem_monitor_realtime (DEVICE_ID,CREDIT_NO,PROD_LINE_ID," \
                                                        "FACILITY_ID,DEVICE_NAME,MONITOR_TIME," \
                                                        "TOTAL_PCC,SYS_CITY_CODE,SYS_COUNTY_CODE) " \
                                                        "values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                    insert_detail_param = (
                                        hashlib.md5(
                                            str((DEVICENAME) + str(hashlib.md5(
                                                (production_line_id + "sc").encode(encoding="utf-8")).hexdigest()) +
                                                str(production_line_id) + str(company_id)).encode(
                                                encoding="utf-8")).hexdigest(),
                                        company_id,
                                        production_line_id,
                                        hashlib.md5(
                                            ((production_line_id + "sc").encode(encoding='utf-8'))).hexdigest(),
                                        DEVICENAME,
                                        itemdict[key]['category'][details],
                                        checkData(YDLs),
                                    '370200000000',
                                    '370212000000'
                                    )

                                    cur.execute(insert_detail_sql, insert_detail_param)
                        connect.commit()
                # 更新程序
                else:
                    if itemdict[key]['zwList'] is not None:
                        for elecScList in range(len(itemdict[key]['zwList'])):
                            # 企业用电更新
                            YDL = itemdict[key]['zwList'][elecScList]['YDL']
                            for details in range(len(YDL)):
                                YDLs = YDL[details]
                                # 工艺线名称
                                DEVICENAME = itemdict[key]['zwList'][elecScList]['DEVICENAME']
                                insert_detail_sql = "update t_cem_monitor_realtime set {} = %s where DEVICE_ID= %s  " \
                                                    "and CREDIT_NO=%s and PROD_LINE_ID=%s and FACILITY_ID=%s and DEVICE_NAME=%s and MONITOR_TIME= %s"
                                insert_detail_sql = insert_detail_sql.format(itemcodename[key])
                                insert_detail_param = (

                                    checkData(YDLs),
                                    hashlib.md5(
                                        str((DEVICENAME) + str(hashlib.md5(
                                            (production_line_id + "sc").encode(encoding="utf-8")).hexdigest()) +
                                            str(production_line_id) + str(company_id)).encode(
                                            encoding="utf-8")).hexdigest(),
                                    CREDIT_NO,
                                    production_line_id,
                                    hashlib.md5(
                                        ((production_line_id + "sc").encode(encoding='utf-8'))).hexdigest(),
                                    DEVICENAME,
                                    itemdict[key]['category'][details],

                                )

                                cur.execute(insert_detail_sql, insert_detail_param)
                        if itemdict[key]['scList'] is not None:
                            for elecScList in range(len(itemdict[key]['scList'])):
                                # 企业治污更新
                                YDL = itemdict[key]['scList'][elecScList]['YDL']
                                for details in range(len(YDL)):
                                    YDLs = YDL[details]
                                    # 工艺线名称
                                    DEVICENAME = itemdict[key]['scList'][elecScList]['DEVICENAME']
                                    insert_detail_sql = "update t_cem_monitor_realtime set {} = %s where DEVICE_ID= %s  " \
                                                        "and CREDIT_NO=%s and PROD_LINE_ID=%s and FACILITY_ID=%s and DEVICE_NAME=%s and MONITOR_TIME= %s"
                                    insert_detail_sql = insert_detail_sql.format(itemcodename[key])
                                    insert_detail_param = (

                                        checkData(YDLs),
                                        hashlib.md5(
                                            str((DEVICENAME) + str(hashlib.md5(
                                                (production_line_id + "sc").encode(encoding="utf-8")).hexdigest()) +
                                                str(production_line_id) + str(company_id)).encode(
                                                encoding="utf-8")).hexdigest(),
                                        CREDIT_NO,
                                        production_line_id,
                                        hashlib.md5(
                                            ((production_line_id + "sc").encode(encoding='utf-8'))).hexdigest(),
                                        DEVICENAME,
                                        itemdict[key]['category'][details],

                                    )

                                    cur.execute(insert_detail_sql, insert_detail_param)
                        connect.commit()
                count = count + 1
                print("执行" + str(count) + "一次")
    except Exception as e:
        print("错误：数据库操作失败", e)
    else:
        connect.commit()
        print("提交成功")


if __name__ == "__main__":
    strs = datetime.datetime.now() - datetime.timedelta(hours=1) - datetime.timedelta(minutes=15)

    time3 = str(strs)

    datetime_obj = datetime.datetime.strptime(time3, "%Y-%m-%d %H:%M:%S.%f")  # 将字符串转换为datetime对象
    new_datetime_obj = datetime_obj.replace(minute=00).replace(microsecond=0).replace(second=0)  # 将microsecond和second替换为0 不为 00开始 则无法获取数据
    requestData(new_datetime_obj)
    time.sleep(5)
    datetime_obj = datetime.datetime.strptime(time3, "%Y-%m-%d %H:%M:%S.%f")  # 将字符串转换为datetime对象
    new_datetime_obj = datetime_obj.replace(minute=15).replace(microsecond=0).replace(second=0)  # 将microsecond和second替换为0 不为 00开始 则无法获取数据
    requestData(new_datetime_obj)
    time.sleep(5)
    datetime_obj = datetime.datetime.strptime(time3, "%Y-%m-%d %H:%M:%S.%f")  # 将字符串转换为datetime对象
    new_datetime_obj = datetime_obj.replace(minute=30).replace(microsecond=0).replace(second=0)  # 将microsecond和second替换为0 不为 00开始 则无法获取数据
    requestData(new_datetime_obj)
    time.sleep(5)
    datetime_obj = datetime.datetime.strptime(time3, "%Y-%m-%d %H:%M:%S.%f")  # 将字符串转换为datetime对象
    new_datetime_obj = datetime_obj.replace(minute=45).replace(microsecond=0).replace(second=0)  # 将microsecond和second替换为0 不为 00开始 则无法获取数据
    requestData(new_datetime_obj)
    time.sleep(5)
    cur.close()  # 关闭游标
    connect.close()
