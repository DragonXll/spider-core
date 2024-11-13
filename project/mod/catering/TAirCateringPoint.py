# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TAirCateringPoint(Base):
    __tablename__ = 't_air_catering_point'
    __table_args__ = (
        Index('index_uni', 'COMPANY_NAME_ALL', 'STATION_ID', 'SYS_CITY_CODE', 'SYS_COUNTY_CODE', unique=True),
        {'comment': '餐饮企业监控点信息'}
    )

    ID = Column(Integer, primary_key=True)
    CREDIT_NO = Column(VARCHAR(50), comment='统一社会信用代码')
    COMPANY_NAME_ALL = Column(VARCHAR(50), comment='监控点名称（企业全称）')
    COMPANY_NAME = Column(VARCHAR(50), comment='餐厅名称（企业简称）')
    AREA_CODE = Column(String(100), comment='区域编码')
    AREA_NAME = Column(String(100), comment='区域名称')
    STATION_ID = Column(VARCHAR(100), comment='排口ID')
    STATION_CODE = Column(VARCHAR(100), comment='排口编码')
    STATION_NAME = Column(VARCHAR(100), comment='排口名称')
    LONGITUDE = Column(DECIMAL(9, 6), comment='中心经度')
    LATITUDE = Column(DECIMAL(9, 6), comment='中心纬度')
    SYS_CREATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
