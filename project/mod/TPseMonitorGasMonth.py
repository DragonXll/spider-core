# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Index, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TPseMonitorGasMonth(Base):
    __tablename__ = 't_pse_monitor_gas_month'
    __table_args__ = (
        Index('index', 'MONITOR_TIME', 'CREDIT_NO', 'OUTPOINT_ID', 'SYS_CITY_CODE', 'SYS_COUNTY_CODE', unique=True),
        {'comment': '污染源_废气(月)'}
    )

    ID = Column(BIGINT, primary_key=True, comment='主键ID')
    MONITOR_TIME = Column(DateTime, index=True, comment='监测时间')
    CREDIT_NO = Column(VARCHAR(128), comment='企业信用代码')
    COMPANY_NAME = Column(VARCHAR(100), index=True, comment='企业名称')
    OUTPOINT_TYPE = Column(VARCHAR(40), comment='排口类型')
    OUTPOINT_ID = Column(BigInteger, comment='排口ID')
    OUTPOINT_NAME = Column(VARCHAR(40), comment='排口名称')
    COMPANY_STATUS = Column(VARCHAR(40), comment='企业状态')
    DEVICE_STATUS = Column(VARCHAR(40), comment='设备状态')
    PID_201 = Column(VARCHAR(30), comment='二氧化硫-PID')
    VAL_201 = Column(VARCHAR(10), comment='二氧化硫-实测值')
    CVT_201 = Column(VARCHAR(10), comment='二氧化硫-折算浓度')
    STAND_201 = Column(VARCHAR(10), comment='二氧化硫-标准值')
    CBBS_201 = Column(VARCHAR(10), comment='二氧化硫-超标倍数')
    EX_201 = Column(VARCHAR(10), comment='二氧化硫-排放量')
    PFL_201 = Column(VARCHAR(10), comment='截止前一日排放量-二氧化硫')
    PID_203 = Column(VARCHAR(10), comment='氮氧化物- PID')
    VAL_203 = Column(VARCHAR(10), comment='氮氧化物-实测值')
    CVT_203 = Column(VARCHAR(10), comment='氮氧化物-折算浓度')
    STAND_203 = Column(VARCHAR(10), comment='氮氧化物-标准值')
    CBBS_203 = Column(VARCHAR(10), comment='氮氧化物-超标倍数')
    EX_203 = Column(VARCHAR(10), comment='氮氧化物-排放量')
    PFL_203 = Column(VARCHAR(10), comment='截止前一日排放量-氮氧化物')
    PID_207 = Column(VARCHAR(10), comment='颗粒物- PID')
    VAL_207 = Column(VARCHAR(10), comment='颗粒物-实测值')
    CVT_207 = Column(VARCHAR(10), comment='颗粒物-折算浓度')
    STAND_207 = Column(VARCHAR(10), comment='颗粒物-标准值')
    CBBS_207 = Column(VARCHAR(10), comment='颗粒物-超标倍数')
    EX_207 = Column(VARCHAR(10), comment='颗粒物-排放量')
    PFL_207 = Column(VARCHAR(10), comment='颗粒物-截止前一日排放量')
    PID_205 = Column(VARCHAR(10), comment='一氧化氮- PID')
    VAL_205 = Column(VARCHAR(10), comment='一氧化氮-实测值')
    CVT_205 = Column(VARCHAR(10), comment='一氧化碳-折算浓度')
    STAND_205 = Column(VARCHAR(10), comment='一氧化碳-标准值')
    CBBS_205 = Column(VARCHAR(10), comment='一氧化碳-超标倍数')
    EX_205 = Column(VARCHAR(10), comment='一氧化碳-排放量')
    PFL_205 = Column(VARCHAR(10), comment='一氧化碳-截止前一日排放总量')
    PID_221 = Column(VARCHAR(10), comment='氯化氢- PID')
    VAL_221 = Column(VARCHAR(10), comment='氯化氢-实测值')
    CVT_221 = Column(VARCHAR(10), comment='氯化氢-折算值')
    STAND_221 = Column(VARCHAR(10), comment='氯化氢-标准值')
    EX_221 = Column(VARCHAR(10), comment='氯化氢-排放量')
    PID_222 = Column(VARCHAR(10), comment='氟化氢- PID')
    VAL_222 = Column(VARCHAR(10), comment='氟化氢-实测值')
    CVT_222 = Column(VARCHAR(10), comment='氟化氢-折算值')
    STAND_222 = Column(VARCHAR(10), comment='氟化氢-标准值')
    EX_222 = Column(VARCHAR(10), comment='氟化氢-排放量')
    VAL_209 = Column(VARCHAR(20), comment='氧气(%)')
    VAL_210 = Column(VARCHAR(20), comment='流量(m3)')
    VAL_211 = Column(VARCHAR(20), comment='流速')
    SYS_CREATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
