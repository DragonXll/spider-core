# coding: utf-8
from sqlalchemy import BigInteger, Column, DECIMAL, DateTime, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TMonitorCar(Base):
    __tablename__ = 't_monitor_car'
    __table_args__ = {'comment': '移动源在线监测_机动车监控分析'}

    ID = Column(BigInteger, primary_key=True)
    RECORD_NO = Column(VARCHAR(50), comment='监测记录编号')
    MONITOR_TYPE = Column(Integer, comment='监测类型（0：遥感遥测监测，1：环检机构监测，2：路检、集中停放抽查）')
    POINT_NO = Column(VARCHAR(255), comment='点位编号')
    POINT_NAME = Column(VARCHAR(255), comment='点位名称')
    AGENCY_NAME = Column(VARCHAR(255), comment='环检机构名称')
    SPOT_CHECK_TYPE = Column(Integer, comment='抽检类型（0：路检抽查1：集中停放抽查）')
    DETECTION_ADDRESS = Column(VARCHAR(255), comment='检测地址')
    LICENSE_PLATE_COLOR = Column(Integer, comment='车牌颜色（0-蓝牌，1-黄牌，2-白牌，3-黑牌，4-新能源，5-其他）')
    LICENSE_PLATE_NUMBER = Column(VARCHAR(20), comment='号码号牌')
    MONITOR_TIME = Column(DateTime, comment='监测时间')
    IS_QUALIFIED = Column(Integer, comment='是否合格（0：不合格，1：合格，2：未判定）')
    CO = Column(DECIMAL(10, 2), comment='CO')
    CO2 = Column(DECIMAL(10, 2), comment='CO2')
    NO = Column(DECIMAL(10, 2), comment='NO')
    HC = Column(DECIMAL(10, 2), comment='HC')
    OPACITY = Column(DECIMAL(10, 2), comment='不透光度')
    RINGMANN_BLACKNESS = Column(DECIMAL(10, 2), comment='林格曼黑度')
    AUDIT_STATUS = Column(Integer, comment='审核状态（0：数据无效，1：数据有效）')
    LONGITUDE = Column(DECIMAL(9, 6), comment='经度')
    LATITUDE = Column(DECIMAL(9, 6), comment='纬度')
    FUEL_TYPE = Column(Integer, comment='燃料种类（0：汽油，1：柴油，2：气体燃料，3：甲醇燃料，4：新能源）')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_STREET_CODE = Column(VARCHAR(20), comment='所属街道编码（实例格式：370212001000）')
    SYS_CREATE_TIME = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
    PROCESSING_STATUS = Column(String(10), comment='处理状态(0：未处理，1：处理)')
    PICTURE_URL = Column(String(255), comment='照片URL')
    IS_LOCAL_CAR = Column(String(10), comment='是否本地车辆（0：否，1：是）')
    CAR_TYPE = Column(String(10), comment='车辆类型（0：轿车，1：SUV）')
    STATION_COUNT = Column(VARCHAR(10), comment='检测工位数量')
    DETECTION_LINE = Column(String(255), comment='检测线')