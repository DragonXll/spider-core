class Kupono:
    countryManifestNo = ''
    receiveEnterpriseName = ''
    receiveAreaName = ''
    transEnterpriseName = ''
    transAreaName = ''
    transportEnterpriseName = ''
    wasteNameStr = ''
    wasteType = ''
    wasteCodeStr = ''
    transferQuantityQuantitySum = ''
    signQuantitySum = ''
    unit = ''
    editedByName = ''
    editedTime = ''
    busiStatus = ''
    progress = ''
    receiveContacts = ''
    transContacts = ''
    receiveContactsTel = ''
    transContactsTel = ''
    receiveLicenceNo = ''
    transIinstCode = ''
    transAddress = ''
    receiveAddress = ''
    transportAddress = ''
    transportQualification = ''
    numberPlate = ''
    transportContacts = ''
    transportContactsTel = ''
    transportCity = ''
    transportLine = ''
    transportMode = ''
    driverName = ''
    driverPhone = ''
    isHandleEnd = '0'
    fileUrl = ''


trans_type = {'CAR': 1, 'TRAIN': 2, 'SHIP': 3, 'PLANE': 4, 'OTHER': 5}

# "code": "WAIT_CONFIRM",
# "name": "待经营确认",

# "code": "WAIT_OUT",
# "name": "待运输出厂",
#
# "code": "WAIT_SIGN",
# "name": "待经营签收",
#
# "code": "WAIT_CONSULT",
# "name": "待签收量协商",
#
# "code": "CONSULT_AGREE",
# "name": "协商同意待签收",
#
# "code": "SIGNED",
# "name": "已签收",
#
# "code": "CANCEL",
# "name": "已作废",
#
# "code": "WAIT_ARRIVE",
# "name": "待运输到厂",
kupono_status = {'WAIT_CONFIRM': 1, 'WAIT_OUT': 2, 'WAIT_SIGN': 3, 'WAIT_CONSULT': 4, 'CONSULT_AGREE': 5,
                 'SIGNED': 6, 'CANCEL': 7, 'WAIT_ARRIVE': 8}
# "arrive"  到厂成功
# "outFactory""  出厂成功
# "finish""  办结成功
# "fillOut""  填领成功
handle_status = {'fillOut': 1, 'outFactory': 2, 'finish': 3}
# 1:成功；2失败
result_type = {'成功': 1, '失败': 2}
# 1=桶;2=槽罐；3=箱；4=编织袋；5=散装；6=其他
containerType = {'1': '桶', '2': '槽罐', '3': '箱', '4': '编织袋', '5': '散装', '6': '其他'}
