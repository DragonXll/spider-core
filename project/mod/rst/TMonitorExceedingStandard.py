# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TMonitorExceedingStandard(Base):
    __tablename__ = 't_monitor_exceeding_standard'
    __table_args__ = {'comment': '移动源在线监测_机动车监控分析_车辆超标'}

    ID = Column(BigInteger, primary_key=True)
    RECORD_NO = Column(VARCHAR(50), comment='监测记录编号')
    CHECK_TYPE = Column(Integer, comment='检测类型（0：遥感遥测、1：环检、2：路检、3：集中停放）')
    LICENSE_PLATE_NUMBER = Column(VARCHAR(20), comment='号码号牌')
    MONITOR_TIME = Column(DateTime, comment='检测时间')
    IS_QUALIFIED = Column(Integer, comment='是否合格（0：否，1：是）')
    EXCEEDING_STANDARD_ITEMS = Column(String(100), comment='超标项目')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_TIME = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
