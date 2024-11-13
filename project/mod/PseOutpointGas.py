
from sqlalchemy import BigInteger, String, Column, DECIMAL, Integer, DateTime, text

from mod import Base


class PseOutpointGas(Base):
    __tablename__ = 't_pse_outpoint_gas'
    __table_args__ = (
        {'comment': '污染源_废气排口'}
    )

    ID = Column(BigInteger, primary_key=True, comment='ID')
    CREDIT_NO = Column(String(64), comment='企业信用代码')
    PSE_ID = Column(BigInteger, comment='污染源表ID')
    OUTPOINT_CODE = Column(String(50), comment='废气排放口代码')
    OUTPOINT_NAME = Column(String(50), comment='废气排放口名称')
    OUTPOINT_POSITION = Column(String(100), comment='排放口位置')
    OUTPOINT_TYPE = Column(String(50), comment='废气排放口类型')
    LONGITUDE = Column(DECIMAL(9, 5), comment='废气排放口经度')
    LATITUDE = Column(DECIMAL(9, 5), comment='废气排放口纬度')
    HEIGHT = Column(DECIMAL(5, 2), comment='废气排放口高度')
    SUB_CODE = Column(String(50), comment='排气筒（排口）编号')
    SUB_NAME = Column(String(100), comment='排气筒（排口）名称')
    SUB_LONGITUDE = Column(DECIMAL(9, 5), comment='排气筒经度')
    SUB_LATITUDE = Column(DECIMAL(9, 5), comment='排气筒纬度')
    SUB_HEIGHT = Column(DECIMAL(5, 2), comment='排气筒高度')
    SUB_SQUARE = Column(DECIMAL(5, 2), comment='排气筒截取面积')
    DEVICE_CODE = Column(String(50), comment='排污设备代码')
    DEVICE_NAME = Column(String(100), comment='排污设备名称')
    STAND = Column(String(50), comment='排放标准')
    STAND_CODE = Column(String(50), comment='排放标准代码')
    RULE_CODE = Column(String(50), comment='废气排放规律代码')
    POINTOUT_STATUS = Column(Integer, comment='排放口状态（0=正常；1=异常）')
    SYS_CREATE_TIME = Column(DateTime(timezone=True), index=True, comment='创建时间')
    SYS_UPDATE_TIME = Column(DateTime(timezone=True), index=True, comment='修改时间')
    SYS_CITY_CODE = Column(String(20), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(String(20), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(String(100), comment='创建人')
    SYS_UPDATE_NAME = Column(String(100), comment='修改人')
