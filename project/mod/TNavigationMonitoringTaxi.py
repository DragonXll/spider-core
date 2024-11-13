# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TNavigationMonitoringTaxi(Base):
    __tablename__ = 't_navigation_monitoring_taxi'
    __table_args__ = {'comment': '走航监测-出租车'}

    ID = Column(BigInteger, primary_key=True)
    TYPE = Column(Integer, comment='数据类型（0：车辆，1：区市，2：街道，3：路段，4：污染点）')
    LICENSE_PLATE_NUMBER = Column(VARCHAR(20), comment='车牌号')
    EQUIPMENT_NO = Column(String(50), comment='设备号')
    ROAD_NO = Column(String(20), comment='道路编号')
    SECTION_NAME = Column(String(50), comment='路段名称')
    STARTING_POINT = Column(String(50), comment='起点')
    END_POINT = Column(String(50), comment='终点')
    ON_LINE = Column(String(255), comment='是否在线 （0=离线； 1=在线）')
    TAXI_SPEED = Column(Float(asdecimal=True), comment='速度')
    POLLUTION_POINT_NAME = Column(String(50), comment='污染点名称')
    MONITOR_TIME = Column(DateTime, comment='监测时间')
    PM2_5 = Column(Float(asdecimal=True), comment='PM2.5')
    PM10 = Column(Float(asdecimal=True), comment='PM10')
    TSP = Column(Float(asdecimal=True), comment='TSP')
    DUST_SOURCE = Column(String(50), comment='降尘源')
    REGION_NAME = Column(VARCHAR(50), comment='所属区县【路段】')
    SYS_STREET_CODE = Column(VARCHAR(20), comment='所属街道编码')
    SYS_STREET_NAME = Column(String(50), comment='所属街道名称')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_TIME = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
