# coding: utf-8
from sqlalchemy import BigInteger, Column, DECIMAL, DateTime, Float, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TMonitorRemoteSenseDetail(Base):
    __tablename__ = 't_monitor_remote_sense_detail'
    __table_args__ = {'comment': '移动源在线监测_机动车监控分析_遥感遥测监测详情报告'}

    ID = Column(BigInteger, primary_key=True)
    RECORD_NO = Column(VARCHAR(50), comment='监测记录编号')
    LONGITUDE = Column(DECIMAL(9, 6), comment='经度')
    LATITUDE = Column(DECIMAL(9, 6), comment='纬度')
    TELEMETRY_LINE_NUMBER = Column(String(20), comment='遥测线编号')
    REMOTE_RECORD_NO = Column(VARCHAR(255), comment='遥感遥测记录编号')
    MONITORING_POINT_LOG_NO = Column(String(255), comment='监测点位日志号')
    MONITORING_PERSON_NAME = Column(String(20), comment='监测人员姓名')
    TRACK_INFO_NO = Column(String(255), comment='轨迹信息编号')
    LICENSE_PLATE_TYPE = Column(Integer, comment='号牌类型（枚举待定）')
    ACCELERATION = Column(Float(asdecimal=True), comment='加速度')
    VEHICLE_SPEED = Column(Float(asdecimal=True), comment='车辆速度')
    FUEL_TYPE = Column(Integer, comment='燃料种类（枚举待定）')
    LANE_NO = Column(Integer, comment='车道号')
    WIND_SPEED = Column(Float(asdecimal=True), comment='风速')
    WIND_DIRECTION = Column(String(20), comment='风向')
    ATMOS = Column(Float(asdecimal=True), comment='大气压')
    HUMIDITY = Column(Float(asdecimal=True), comment='湿度')
    AMBIENT_HUMIDITY = Column(Float(asdecimal=True), comment='环境湿度')
    LANE_SLOPE = Column(Float(asdecimal=True), comment='车道坡度')
    CO2 = Column(DECIMAL(10, 2), comment='CO2')
    VSP = Column(DECIMAL(10, 2), comment='VSP')
    CO_LIMIT = Column(DECIMAL(10, 2), comment='CO限值')
    CO_CO2_RATE = Column(Float(asdecimal=True), comment='CO与CO2比率')
    CO_POLLUTION_RESULT = Column(Integer, comment='CO排放判定（0：合格，1：不合格）')
    NO_LIMIT = Column(DECIMAL(10, 2), comment='NO限值')
    NO_CO2_RATE = Column(Float(asdecimal=True), comment='NO与CO2比率')
    NO_POLLUTION_RESULT = Column(Integer, comment='NO排放判定（0：合格，1：不合格）')
    REMARK = Column(String(255), comment='备注')
    APPROVED_DATE = Column(DateTime, comment='审核日期')
    APPROVED_STATUS = Column(Integer, comment='审核状态（枚举待定）')
    APPROVED_PERSON_NAME = Column(String(20), comment='审核人')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_TIME = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
