# coding: utf-8
from sqlalchemy import BigInteger, Column, DECIMAL, DateTime, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TLandInfo(Base):
    __tablename__ = 't_land_info'
    __table_args__ = {'comment': '地块信息'}

    ID = Column(BigInteger, primary_key=True)
    LAND_NAME = Column(String(255), comment='地块名称')
    LAND_NO = Column(String(255), comment='地块编号')
    POSITION = Column(String(255), comment='地块位置')
    LONGITUDE = Column(DECIMAL(9, 6), comment='经度')
    LATITUDE = Column(DECIMAL(9, 6), comment='纬度')
    RANGE = Column(String(255), comment='四至范围')
    AREA = Column(String(255), comment='地块面积（㎡）')
    BUSINESS_TYPE = Column(String(255), comment='行业类型')
    LAND_TYPE = Column(String(255), comment='地块类型')
    PLANNED_USE = Column(String(255), comment='规划用途')
    TEL = Column(String(255), comment='联系方式')
    STATE = Column(String(255), comment='所处阶段')
    SURVEY_BASIS = Column(String(255), comment='调查依据')
    IS_POLLUTED = Column(String(255), comment='是否污染')
    USER_RIGHT_HOLDER = Column(VARCHAR(255), comment='土地使用权人（政府）')
    CREDIT_NO = Column(VARCHAR(64), comment='统一社会信用代码')
    RECYCLING_DATE = Column(DateTime, comment='回收土地使用权日期')
    FORMER_USER_RIGHT_HOLDER = Column(String(255), comment='前任土地使用权人（政府）')
    FORMER_CREDIT_NO = Column(VARCHAR(64), comment='统一社会信用代码')
    MULTIPLE_USER_RIGHT_HOLDER = Column(String(255), comment='现任多土地使用权人')
    FORMER_MULTIPLE_USER_RIGHT_HOLDER = Column(String(255), comment='前任多土地使用权人')
    COORDINATE_SYSTEM_DESCRIPTION = Column(String(255), comment='坐标系说明')
    LEGAL_NAME = Column(VARCHAR(50), comment='法人代表')
    CONTACT = Column(String(255), comment='联系人')
    ZIP_CODE = Column(String(255), comment='邮编')
    POLICY_BASIS = Column(String(255), comment='政策依据')
    INVOLVED_WORK = Column(String(255), comment='涉及的专项工作')
    INVOLVED_AREA = Column(String(255), comment='涉及的重点区域')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属区县编码（实例格式：370212000000）')
    SYS_STREET_CODE = Column(VARCHAR(20), comment='所属街道编码（实例格式：370212001000）')
    SYS_CREATE_TIME = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
