from datetime import datetime

import requests
from sqlalchemy.orm import Session

from database.mysql import get_soil_db
from job.soil.ls_soil_login import getTicket
from mod.soil.TLandInfo import TLandInfo


def getLandInfo():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'http://103.239.155.212:30038/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/125.0.0.0 Safari/537.36',
    }

    params = {
        'pagingParams': '{"pageIndex":1,"pageSize":50}',
        'queryParams': '{"area":"","city":"","isMoveOutDirectoryOfSurveysList":[],"isReportStatList":[],"keyword":"",'
                       '"timeType":"","month":"2024-06-07 13:51:58","year":"","beginTime":"2023-12-07 13:51:59",'
                       '"endTime":"2024-06-07 13:51:58","province":"370000","isMoveOutDirectoryOfSurveys":"",'
                       '"isReportStat":"","isInvestigateList":"1"}',
        'ticket': getTicket(),
    }

    response = requests.get(
        'http://103.239.155.212:30039/shencai-soil-web/service/soil/landManagement/tSoilLandInfoModel'
        '/queryPageTSoilLandInfoModel',
        params=params,
        headers=headers,
        verify=False,
    )
    land_info_list = response.json()['data']['dataList']
    print(land_info_list)
    db: Session = next(get_soil_db())
    for land_info in land_info_list:
        # 检查LAND_NO是否已存在
        existing_land_info = db.query(TLandInfo).filter_by(LAND_NO=land_info['landNumber']).one_or_none()
        if existing_land_info:
            print(f"地块编号 {land_info['landNumber']} 已存在，跳过此记录。")
            continue  # 如果存在，则跳过当前循环继续下一个
        new_land_info = TLandInfo(
            # 地块名称
            LAND_NAME=land_info['landName'],
            # 地块编号
            LAND_NO=land_info['landNumber'],
            # 地块位置
            POSITION=land_info['landAddress'],
            # 经度
            LONGITUDE=float(land_info['lon']) if land_info['lon'] else 0.0,
            # 纬度
            LATITUDE=float(land_info['lat']) if land_info['lat'] else 0.0,
            # 四至范围
            RANGE=land_info['fourBoundaries'],
            # 地块面积
            AREA=land_info['area'],
            # 行业类型
            BUSINESS_TYPE=land_info['industryName'],
            # 地块类型
            LAND_TYPE=land_info['landType'],
            # 规划用途
            PLANNED_USE=land_info['remark'],
            # 联系方式
            TEL=land_info['landContact'],
            # 所处阶段
            STATE=land_info['stageName'],
            # 调查依据
            SURVEY_BASIS=land_info['checkedCities'],
            # 是否污染
            IS_POLLUTED=land_info['isExceedName'],
            # 土地使用权人（政府）
            USER_RIGHT_HOLDER=land_info['landUser'],
            # 统一社会信用代码
            CREDIT_NO=land_info['formerUniformSocialCreditCode'],
            # 回收土地使用权日期
            RECYCLING_DATE=land_info['inquiryEndTime'],
            # 前任土地使用权人（政府）
            FORMER_USER_RIGHT_HOLDER=land_info['exUser'],
            # 统一社会信用代码
            FORMER_CREDIT_NO=land_info['formerUniformSocialCreditCode'],
            # 现任多土地使用权人
            MULTIPLE_USER_RIGHT_HOLDER='',
            # 前任多土地使用权人
            FORMER_MULTIPLE_USER_RIGHT_HOLDER='',
            # 坐标系说明
            COORDINATE_SYSTEM_DESCRIPTION='',
            # 法人代表
            LEGAL_NAME=land_info['legalRepresentative'],
            # 联系人
            CONTACT=land_info['landContact'],
            # 邮编
            ZIP_CODE=land_info['postCode'],
            # 政策依据
            POLICY_BASIS=land_info['checkedCitie'],
            # 涉及的专项工作
            INVOLVED_WORK='',
            # 涉及的重点区域
            INVOLVED_AREA='',
            # 所属地级市编码（实例格式：370200000000）
            SYS_CITY_CODE='370200000000',
            # 所属区县编码（实例格式：370212000000）
            SYS_COUNTY_CODE='370212000000',
            # 所属街道编码（实例格式：370212001000）
            SYS_STREET_CODE='',
            # 创建时间
            SYS_CREATE_TIME=datetime.now(),
        )
        # 插入数据库
        db.merge(new_land_info)
    db.commit()
    db.close()


if __name__ == '__main__':
    getLandInfo()
