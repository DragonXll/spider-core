# coding: utf-8
from sqlalchemy import BigInteger, Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TAirCateringWarn(Base):
    __tablename__ = 't_air_catering_warn'
    __table_args__ = {'comment': '餐饮油烟_告警'}

    ID = Column(BigInteger, primary_key=True, comment='主键ID')
    COMPANY_NAME = Column(VARCHAR(50), comment='餐厅名称')
    AREA_CODE = Column(VARCHAR(100), comment='区域编码')
    AREA_NAME = Column(VARCHAR(100), comment='区域名称')
    STATION_ID = Column(VARCHAR(100), comment='排口ID')
    STATION_NAME = Column(VARCHAR(100), comment='排口名称')
    MEASURED_INDEX = Column(String(50), comment='监测指标')
    EXCEEDING_DURATION = Column(String(50), comment='超标时长')
    START_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='开始时间')
    END_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='结束时间')
    ALARM_STATUS = Column(String(10), comment='报警状态')
    PURIFIER_ON_TIME = Column(String(50), comment='净化器开启时长')
    PURIFIER_FAULT_TIME = Column(String(50), comment='净化器故障时长')
    EXCESS_REASON = Column(VARCHAR(100), comment='超标原因')
    SYS_CREATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
