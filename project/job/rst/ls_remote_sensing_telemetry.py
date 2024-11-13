from datetime import datetime

import requests
import argparse
from sqlalchemy.orm import Session

from database.mysql import get_air_db
from mod.rst.TMonitorCar import TMonitorCar
from mod.rst.TMonitorExceedingStandard import TMonitorExceedingStandard
from mod.rst.TMonitorRemoteSenseDetail import TMonitorRemoteSenseDetail


def getMonitorCar():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/125.0.0.0 Safari/537.36',
    }

    params = {
        'token': '',
        'STARTTIME': '',
        'thsRegionCode': '',
        'ENDTIME': '',
    }

    response = requests.get(
        'http://10.0.253.5:7080/serviceinterface/search/run.action?interfaceId=8bb26023-4fa8-8b40-7e48-4d7ca297740f',
        params=params,
        headers=headers,
        verify=False,
    )
    data_list = response.json()['data']
    print(data_list)
    db: Session = next(get_air_db())
    for data in data_list:
        # 检查数据是否重复
        existing_data = db.query(TMonitorCar).filter_by(RECORD_NO=data['JLBH']).filter_by(MONITOR_TYPE=0).one_or_none()
        if existing_data:
            print(f"遥测数据记录'{data['JLBH']} 已存在，跳过此记录")
            continue
        monitor_car = TMonitorCar(
            # 监测记录编号
            RECORD_NO=data['JLBH'],
            # 0：遥感遥测监测
            MONITOR_TYPE=0,
            # 点位编号
            POINT_NO=data['DWBH'],
            # 点位名称
            POINT_NAME=data['DWMC'],
            # 环检机构名称
            AGENCY_NAME=data['无'],
            # 抽检类型（0：路检抽查1：集中停放抽查）                
            SPOT_CHECK_TYPE=0,
            # 检测地址
            DETECTION_ADDRESS=data['LXDZ'],
            # 车牌颜色（0-蓝牌，1-黄牌，2-白牌，3-黑牌，4-新能源，5-其他）
            LICENSE_PLATE_COLOR=data['CPYS'],
            # 号码号牌
            LICENSE_PLATE_NUMBER=data['HPHM'],
            # 监测时间
            MONITOR_TIME=data['JCRQ'],
            # 是否合格（0：不合格，1：合格，2：未判定）
            IS_QUALIFIED=data['PDJG'],
            # CO
            CO=data['COJG'],
            # CO2
            CO2=data['CO2JG'],
            # NO
            NO=data['NOJG'],
            # HC
            HC=data['HCJG'],
            # 不透光度
            OPACITY=data['BTGDJG'],
            # 林格曼黑度
            RINGMANN_BLACKNESS=data['LGMHD'],
            # 审核状态（0：数据无效，1：数据有效
            AUDIT_STATUS=data['ZT'],
            # 经度
            LONGITUDE=float(data['DDJD']) if data['DDJD'] else 0.0,
            # 纬度
            LATITUDE=float(data['DDWD']) if data['DDJD'] else 0.0,
            # 燃料种类（0：汽油，1：柴油，2：气体燃料，3：甲醇燃料，4：新能源）
            FUEL_TYPE=data['RLZL'],
            # 所属地级市编码（实例格式：370200000000）
            SYS_CITY_CODE='370200000000',
            # 所属区县编码（实例格式：370283000000）
            SYS_COUNTY_CODE='370212000000',
            # 所属街道编码（实例格式：370212001000）
            SYS_STREET_CODE='',
            # 创建时间
            SYS_CREATE_TIME=datetime.now(),
            # 修改时间
            SYS_UPDATE_TIME='',
            # 创建人
            SYS_CREATE_NAME='',
            # 修改人
            SYS_UPDATE_NAME='',
            # 处理状态(0：未处理，1：处理)
            PROCESSING_STATUS=0,
            # 照片URL
            PICTURE_URL='',
            # 是否本地车辆（0：否，1：是）
            IS_LOCAL_CAR=0,
            # 车辆类型（0：轿车，1：SUV）
            CAR_TYPE=data['CLLX'],
            # 检测工位数量
            STATION_COUNT='无',
            # 检测线
            DETECTION_LINE='无'
        )
        # 插入数据库
        db.merge(monitor_car)
    db.commit()
    db.close()


def getMonitorExceedingStandard():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/125.0.0.0 Safari/537.36',
    }

    params = {
        'token': '',
        'STARTTIME': '',
        'thsRegionCode': '',
        'ENDTIME': '',
    }

    response = requests.get(
        'http://10.0.253.5:7080/serviceinterface/search/run.action?interfaceId=8bb26023-4fa8-8b40-7e48-4d7ca297740f',
        params=params,
        headers=headers,
        verify=False,
    )
    data_list = response.json()['data']
    print(data_list)
    db: Session = next(get_air_db())
    for data in data_list:
        # 检查数据是否重复
        existing_data = db.query(TMonitorExceedingStandard).filter_by(RECORD_NO=data['JLBH']).filter_by(
            CHECK_TYPE=0).one_or_none()
        if existing_data:
            print(f"遥测数据超标记录'{data['JLBH']} 已存在，跳过此记录")
            continue
        exceed_list = []
        if float(data['COJG']) > float(data['COXZ']):
            exceed_list.append('CO')
        if float(data['HCJG']) > float(data['HCXZ']):
            exceed_list.append('HC')
        if float(data['NOJG']) > float(data['NOXZ']):
            exceed_list.append('NO')
        monitor_exceeding_standard = TMonitorExceedingStandard(
            # 监测记录编号
            RECORD_NO=data['JLBH'],
            # 检测类型（0：遥感遥测、1：环检、2：路检、3：集中停放）
            CHECK_TYPE=0,
            # 号码号牌
            LICENSE_PLATE_NUMBER=data['HPHM'],
            # 检测时间
            MONITOR_TIME=data['JCRQ'],
            # 是否合格（0：否，1：是）
            IS_QUALIFIED=data['PDJG'],
            # 超标项目 设置一个数组判断值
            EXCEEDING_STANDARD_ITEMS=exceed_list,
            # 所属地级市编码（实例格式：370200000000）
            SYS_CITY_CODE='370200000000',
            # 所属区县编码（实例格式：370283000000）
            SYS_COUNTY_CODE='370212000000',
            # 创建时间
            SYS_CREATE_TIME=datetime.now(),
            # 修改时间
            SYS_UPDATE_TIME='',
            # 创建人
            SYS_CREATE_NAME='',
            # 修改人
            SYS_UPDATE_NAME='',
        )
        db.add(monitor_exceeding_standard)
    db.commit()
    db.close()


def getMonitorRemoteSenseDetail():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/125.0.0.0 Safari/537.36',
    }

    params = {
        'token': '',
        'STARTTIME': '',
        'thsRegionCode': '',
        'ENDTIME': '',
    }

    response = requests.get(
        'http://10.0.253.5:7080/serviceinterface/search/run.action?interfaceId=8bb26023-4fa8-8b40-7e48-4d7ca297740f',
        params=params,
        headers=headers,
        verify=False,
    )
    data_list = response.json()['data']
    print(data_list)
    db: Session = next(get_air_db())
    for data in data_list:
        # 检查数据是否重复
        existing_data = db.query(TMonitorRemoteSenseDetail).filter_by(RECORD_NO=data['JLBH']).one_or_none()
        if existing_data:
            print(f"遥测数据详情记录'{data['JLBH']} 已存在，跳过此记录")
            continue
        remote_sense = TMonitorRemoteSenseDetail(
            # 监测记录编号
            RECORD_NO=data['JLBH'],
            # 经度
            LONGITUDE=float(data['DDJD']) if data['DDJD'] else 0.0,
            # 纬度
            LATITUDE=float(data['DDWD']) if data['DDJD'] else 0.0,
            # 遥测线编号
            TELEMETRY_LINE_NUMBER=data['YCXBH'],
            # 遥感遥测记录编号
            REMOTE_RECORD_NO=data['JLBH'],
            # 监测点位日志号
            MONITORING_POINT_LOG_NO=data['JCDWRZH'],
            # 监测人员姓名
            MONITORING_PERSON_NAME=data['JCRYXM'],
            # 轨迹信息编号
            TRACK_INFO_NO=data['GJXXBH'],
            # 号牌类型（枚举待定）
            LICENSE_PLATE_TYPE=data['HPZL'],
            # 加速度
            ACCELERATION=data['CLJSD'],
            # 车辆速度
            VEHICLE_SPEED=data['CLSD'],
            # 燃料种类（枚举待定）
            FUEL_TYPE=data['RLZL'],
            # 车道号
            LANE_NO=data['CDXH'],
            # 风速
            WIND_SPEED=data['FS'],
            # 风向
            WIND_DIRECTION=data['FX'],
            # 大气压
            ATMOS=data['DQY'],
            # 湿度
            HUMIDITY=data['SD'],
            # 环境湿度
            AMBIENT_HUMIDITY=data['HJWD'],
            # 车道坡度
            LANE_SLOPE=data['CDPD'],
            # CO2
            CO2=data['CO2JG'],
            # VSP
            VSP=data['VSP'],
            # CO限值
            CO_LIMIT=data['COXZ'],
            # CO与CO2比率
            CO_CO2_RATE=data['COCO2'],
            # CO排放判定（0：合格，1：不合格）
            CO_POLLUTION_RESULT=0 if float(data['COJG'] < float(data['COXZ'])) else 1,
            # NO限值
            NO_LIMIT=data['NOXZ'],
            # NO与CO2比率
            NO_CO2_RATE=data['NOCO2'],
            # NO排放判定（0：合格，1：不合格）
            NO_POLLUTION_RESULT=0 if float(data['NOJG'] < float(data['NOXZ'])) else 1,
            #  备注
            REMARK='',
            #  审核日期
            APPROVED_DATE=data['SHRQ'],
            #  审核状态（枚举待定）
            APPROVED_STATUS=data['ZT'],
            #  审核人
            APPROVED_PERSON_NAME=data['SHR'],
            # 所属地级市编码（实例格式：370200000000）
            SYS_CITY_CODE='370200000000',
            # 所属区县编码（实例格式：370283000000）
            SYS_COUNTY_CODE='370212000000',
            # 创建时间
            SYS_CREATE_TIME=datetime.now(),
            # 修改时间
            SYS_UPDATE_TIME='',
            # 创建人
            SYS_CREATE_NAME='',
            # 修改人
            SYS_UPDATE_NAME=''
        )
        db.add(remote_sense)
    db.commit()
    db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='解析参数')
    parser.add_argument('--dateType', '-d', type=int, help='类型(1,2,3)', choices=[1, 2, 3])  # 添加type和choices以限制输入类型和选项
    args = parser.parse_args()
    if args.dateType == 1:
        getMonitorCar()
    elif args.dateType == 2:
        getMonitorExceedingStandard()
    elif args.dateType == 3:
        getMonitorRemoteSenseDetail()
    else:
        print("无效的dateType参数。请输入1,2,3")
