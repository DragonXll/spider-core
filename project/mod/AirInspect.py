# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TAirInspect(Base):
    __tablename__ = 't_air_inspect'
    __table_args__ = (
        Index('ids_index', 'CREDIT_NO', 'MONITOR_TIME', 'OUTPOINT_CODE', 'PROJECT_NAME', 'SYS_COUNTY_CODE', 'SYS_CITY_CODE', unique=True),
        {'comment': '重点监管企业例行监测'}
    )

    ID = Column(BigInteger, primary_key=True)
    CREDIT_NO = Column(VARCHAR(64), comment='统一社会信用代码【MD5】')
    COMPANY_NAME = Column(VARCHAR(100), comment='企业名称')
    MONITOR_TIME = Column(DateTime, comment='监测时间')
    OUTPOINT_CODE = Column(VARCHAR(50), comment='废气排放口代码')
    OUTPOINT_NAME = Column(VARCHAR(50), comment='废气排放口名称')
    MONITOR_TYPE = Column(String(10), comment='监测类型')
    PROJECT_NAME = Column(VARCHAR(50), comment='项目名称')
    MONITOR_VALUE = Column(String(20), comment='监测值')
    MONITOR_STANDARD = Column(String(20), comment='标准值')
    IS_PASS = Column(Integer, server_default=text("'0'"), comment='是否超标（0=正常；1=超标）')
    SYS_CREATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
