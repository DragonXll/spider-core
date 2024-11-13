# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Index, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class PseMonitorWaterDay(Base):
    __tablename__ = 't_pse_monitor_water_day'
    __table_args__ = (
        Index('index', 'MONITOR_TIME', 'CREDIT_NO', 'OUTPOINT_ID', 'SYS_CITY_CODE', 'SYS_COUNTY_CODE'),
        {'comment': '污染源_废水(天数据)'}
    )

    ID = Column(BIGINT, primary_key=True, comment='主键ID')
    MONITOR_TIME = Column(DateTime, comment='监测时间')
    CREDIT_NO = Column(VARCHAR(128), comment='企业信用代码')
    COMPANY_NAME = Column(VARCHAR(100), comment='企业名称')
    OUTPOINT_TYPE = Column(VARCHAR(40), comment='排口类型')
    OUTPOINT_ID = Column(BigInteger, comment='排口ID')
    OUTPOINT_NAME = Column(VARCHAR(40), comment='排口名称')
    COMPANY_STATUS = Column(VARCHAR(40), comment='企业状态')
    DEVICE_STATUS = Column(VARCHAR(40), comment='设备状态')
    C0007_AO = Column(VARCHAR(10))
    CS_STATE = Column(VARCHAR(100))
    ZT_STATE = Column(VARCHAR(100))
    PID_301 = Column(VARCHAR(100))
    VAL_301 = Column(VARCHAR(100), comment='水温-实测值')
    STAND_301 = Column(VARCHAR(100))
    STAND_LOW_301 = Column(VARCHAR(100))
    CBBS_301 = Column(VARCHAR(100))
    LOW_301 = Column(VARCHAR(100))
    HIGH_301 = Column(VARCHAR(100))
    LOWER_LIMIT_301 = Column(VARCHAR(100))
    PFL_301 = Column(VARCHAR(100))
    PID_316 = Column(VARCHAR(100))
    VAL_316 = Column(VARCHAR(100), comment='化学需氧量-实测值')
    STAND_316 = Column(VARCHAR(100))
    STAND_LOW_316 = Column(VARCHAR(100))
    CBBS_316 = Column(VARCHAR(100))
    LOW_316 = Column(VARCHAR(100))
    HIGH_316 = Column(VARCHAR(100))
    LOWER_LIMIT_316 = Column(VARCHAR(100))
    PFL_316 = Column(VARCHAR(100))
    PID_311 = Column(VARCHAR(100))
    VAL_311 = Column(VARCHAR(100), comment='氨氮-实测值')
    STAND_311 = Column(VARCHAR(100))
    STAND_LOW_311 = Column(VARCHAR(100))
    CBBS_311 = Column(VARCHAR(100))
    LOW_311 = Column(VARCHAR(100))
    HIGH_311 = Column(VARCHAR(100))
    LOWER_LIMIT_311 = Column(VARCHAR(100))
    PFL_311 = Column(VARCHAR(100))
    PID_302 = Column(VARCHAR(100))
    VAL_302 = Column(VARCHAR(100), comment='PH-实测值')
    STAND_302 = Column(VARCHAR(100))
    STAND_LOW_302 = Column(VARCHAR(100))
    CBBS_302 = Column(VARCHAR(100))
    LOW_302 = Column(VARCHAR(100))
    HIGH_302 = Column(VARCHAR(100))
    LOWER_LIMIT_302 = Column(VARCHAR(100))
    PFL_302 = Column(VARCHAR(100))
    PID_495 = Column(VARCHAR(100))
    VAL_495 = Column(VARCHAR(100), comment='累计流量-实测值')
    STAND_495 = Column(VARCHAR(100))
    STAND_LOW_495 = Column(VARCHAR(100))
    CBBS_495 = Column(VARCHAR(100))
    LOW_495 = Column(VARCHAR(100))
    HIGH_495 = Column(VARCHAR(100))
    LOWER_LIMIT_495 = Column(VARCHAR(100))
    PFL_495 = Column(VARCHAR(100))
    PID_313 = Column(VARCHAR(100))
    VAL_313 = Column(VARCHAR(100), comment='总磷-实测值')
    STAND_313 = Column(VARCHAR(100))
    STAND_LOW_313 = Column(VARCHAR(100))
    CBBS_313 = Column(VARCHAR(100))
    LOW_313 = Column(VARCHAR(100))
    HIGH_313 = Column(VARCHAR(100))
    LOWER_LIMIT_313 = Column(VARCHAR(100))
    PFL_313 = Column(VARCHAR(100))
    PID_466 = Column(VARCHAR(100))
    VAL_466 = Column(VARCHAR(100), comment='总氮-实测值')
    STAND_466 = Column(VARCHAR(100))
    STAND_LOW_466 = Column(VARCHAR(100))
    CBBS_466 = Column(VARCHAR(100))
    LOW_466 = Column(VARCHAR(100))
    HIGH_466 = Column(VARCHAR(100))
    LOWER_LIMIT_466 = Column(VARCHAR(100))
    PFL_466 = Column(VARCHAR(100))
    PID_323 = Column(VARCHAR(100))
    VAL_323 = Column(VARCHAR(100), comment='铬(六价)-实测值')
    STAND_323 = Column(VARCHAR(100))
    STAND_LOW_323 = Column(VARCHAR(100))
    CBBS_323 = Column(VARCHAR(100))
    LOW_323 = Column(VARCHAR(100))
    HIGH_323 = Column(VARCHAR(100))
    LOWER_LIMIT_323 = Column(VARCHAR(100))
    PFL_323 = Column(VARCHAR(100))
    PID_470 = Column(VARCHAR(100))
    VAL_470 = Column(VARCHAR(100), comment='总铬-实测值')
    STAND_470 = Column(VARCHAR(100))
    STAND_LOW_470 = Column(VARCHAR(100))
    CBBS_470 = Column(VARCHAR(100))
    LOW_470 = Column(VARCHAR(100))
    HIGH_470 = Column(VARCHAR(100))
    LOWER_LIMIT_470 = Column(VARCHAR(100))
    PFL_470 = Column(VARCHAR(100))
    PID_331 = Column(VARCHAR(100))
    VAL_331 = Column(VARCHAR(100), comment='总镍-实测值')
    STAND_331 = Column(VARCHAR(100))
    STAND_LOW_331 = Column(VARCHAR(100))
    CBBS_331 = Column(VARCHAR(100))
    LOW_331 = Column(VARCHAR(100))
    HIGH_331 = Column(VARCHAR(100))
    LOWER_LIMIT_331 = Column(VARCHAR(100))
    PFL_331 = Column(VARCHAR(100))
    PID_324 = Column(VARCHAR(100))
    VAL_324 = Column(VARCHAR(100), comment='总铅-实测值')
    STAND_324 = Column(VARCHAR(100))
    STAND_LOW_324 = Column(VARCHAR(100))
    CBBS_324 = Column(VARCHAR(100))
    LOW_324 = Column(VARCHAR(100))
    HIGH_324 = Column(VARCHAR(100))
    LOWER_LIMIT_324 = Column(VARCHAR(100))
    PFL_324 = Column(VARCHAR(100))
    PID_308 = Column(VARCHAR(100))
    VAL_308 = Column(VARCHAR(100), comment='总锌-实测值')
    STAND_308 = Column(VARCHAR(100))
    STAND_LOW_308 = Column(VARCHAR(100))
    CBBS_308 = Column(VARCHAR(100))
    LOW_308 = Column(VARCHAR(100))
    HIGH_308 = Column(VARCHAR(100))
    LOWER_LIMIT_308 = Column(VARCHAR(100))
    PFL_308 = Column(VARCHAR(100))
    PID_320 = Column(VARCHAR(100))
    VAL_320 = Column(VARCHAR(100), comment='总砷-实测值')
    STAND_320 = Column(VARCHAR(100))
    STAND_LOW_320 = Column(VARCHAR(100))
    CBBS_320 = Column(VARCHAR(100))
    LOW_320 = Column(VARCHAR(100))
    HIGH_320 = Column(VARCHAR(100))
    LOWER_LIMIT_320 = Column(VARCHAR(100))
    PFL_320 = Column(VARCHAR(100))
    DATA_TIME_302 = Column(VARCHAR(100))
    DATA_TIME_316 = Column(VARCHAR(100))
    DATA_TIME_495 = Column(VARCHAR(100))
    DATA_TIME_311 = Column(VARCHAR(100))
    DATA_TIME_313 = Column(VARCHAR(100))
    DATA_TIME_466 = Column(VARCHAR(100))
    SYS_CREATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
    EX_316 = Column(VARCHAR(20), comment='排放量')
    SOURCE_316 = Column(VARCHAR(20), comment='来源')
    STATUS_316 = Column(VARCHAR(20), comment='状态')
    EX_311 = Column(VARCHAR(20), comment='排放量')
    SOURCE_311 = Column(VARCHAR(20), comment='来源')
    STATUS_311 = Column(VARCHAR(20), comment='状态')
    EX_313 = Column(VARCHAR(20), comment='排放量')
    SOURCE_313 = Column(VARCHAR(20), comment='来源')
    STATUS_313 = Column(VARCHAR(20), comment='状态')
    EX_466 = Column(VARCHAR(20), comment='排放量')
    SOURCE_466 = Column(VARCHAR(20), comment='来源')
    STATUS_466 = Column(VARCHAR(20), comment='状态')
    EX_470 = Column(VARCHAR(20), comment='排放量')
    SOURCE_470 = Column(VARCHAR(20), comment='来源')
    STATUS_470 = Column(VARCHAR(20), comment='状态')
    EX_323 = Column(VARCHAR(20), comment='排放量')
    SOURCE_323 = Column(VARCHAR(20), comment='来源')
    STATUS_323 = Column(VARCHAR(20), comment='状态')
    EX_331 = Column(VARCHAR(20), comment='排放量')
    SOURCE_331 = Column(VARCHAR(20), comment='来源')
    STATUS_331 = Column(VARCHAR(20), comment='状态')
    EX_302 = Column(VARCHAR(20), comment='排放量')
    SOURCE_302 = Column(VARCHAR(20), comment='来源')
    STATUS_302 = Column(VARCHAR(20), comment='状态')
    EX_324 = Column(VARCHAR(20), comment='排放量')
    SOURCE_324 = Column(VARCHAR(20), comment='来源')
    STATUS_324 = Column(VARCHAR(20), comment='状态')
    EX_318 = Column(VARCHAR(20), comment='排放量')
    SOURCE_318 = Column(VARCHAR(20), comment='来源')
    STATUS_318 = Column(VARCHAR(20), comment='状态')
    EX_307 = Column(VARCHAR(20), comment='排放量')
    SOURCE_307 = Column(VARCHAR(20), comment='来源')
    STATUS_307 = Column(VARCHAR(20), comment='状态')
    EX_308 = Column(VARCHAR(20), comment='排放量')
    SOURCE_308 = Column(VARCHAR(20), comment='来源')
    STATUS_308 = Column(VARCHAR(20), comment='状态')
    EX_320 = Column(VARCHAR(20), comment='排放量')
    SOURCE_320 = Column(VARCHAR(20), comment='来源')
    STATUS_320 = Column(VARCHAR(20), comment='状态')
    EX_325 = Column(VARCHAR(20), comment='排放量')
    SOURCE_325 = Column(VARCHAR(20), comment='来源')
    STATUS_325 = Column(VARCHAR(20), comment='状态')
    EX_301 = Column(VARCHAR(20), comment='排放量')
    SOURCE_301 = Column(VARCHAR(20), comment='来源')
    STATUS_301 = Column(VARCHAR(20), comment='状态')
    EX_494 = Column(VARCHAR(20), comment='排放量')
    SOURCE_494 = Column(VARCHAR(20), comment='来源')
    STATUS_494 = Column(VARCHAR(20), comment='状态')
    VAL_318 = Column(VARCHAR(255))
    STAND_318 = Column(VARCHAR(255))
    VAL_307 = Column(VARCHAR(255))
    STAND_307 = Column(VARCHAR(255))
    VAL_325 = Column(VARCHAR(255))
    STAND_325 = Column(VARCHAR(255))
    VAL_494 = Column(VARCHAR(255))
    STAND_494 = Column(VARCHAR(255))
