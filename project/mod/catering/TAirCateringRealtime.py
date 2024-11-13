# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TAirCateringRealtime(Base):
    __tablename__ = 't_air_catering_realtime'
    __table_args__ = {'comment': '餐饮油烟_监控数据【实时】'}

    id = Column(BigInteger, primary_key=True)
    CREDIT_NO = Column(VARCHAR(64), comment='统一社会信用代码')
    COMPANY_NAME = Column(VARCHAR(50), comment='餐厅名称')
    STATION_ID = Column(VARCHAR(100), comment='排口ID')
    STATION_NAME = Column(VARCHAR(100), comment='排口名称')
    MONITOR_TIME = Column(DateTime, comment='监测时间')
    DETECTION_STATUS = Column(Integer, comment='检测状态（0：正常 1：超标 2：离线  3：冻结）')
    LINKAGE_RATIO = Column(VARCHAR(50), comment='联动比')
    PURIFIER_STATUS = Column(Integer, comment='净化器状态（0=不在线；1=在线）')
    FAN_STATUS = Column(Integer, comment='风机状态（0=不在线；1=在线）')
    A34041 = Column(VARCHAR(50), comment='油烟浓度（A34041）')
    A01002 = Column(VARCHAR(50), comment='颗粒物（A01002）')
    A01001 = Column(VARCHAR(50), nullable=False, comment='非甲烷总烃（A01001）')
    SYS_CREATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
