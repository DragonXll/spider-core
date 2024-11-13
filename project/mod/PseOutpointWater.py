from sqlalchemy import BigInteger, Column, DECIMAL, Index, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class PseOutpointWater(Base):
    __tablename__ = 't_pse_outpoint_water'
    __table_args__ = (
        Index('index', 'PSE_ID', 'CREDIT_NO', 'OUTPOINT_CODE', 'SYS_CITY_CODE', 'SYS_COUNTY_CODE'),
        {'comment': '污染源_废水排口'}
    )

    ID = Column(BigInteger, primary_key=True, comment='ID')
    PSE_ID = Column(BigInteger, comment='污染源表ID')
    CREDIT_NO = Column(VARCHAR(64), comment='企业信用代码')
    OUTPOINT_CODE = Column(VARCHAR(50), comment='废水排放口代码')
    OUTPOINT_NAME = Column(VARCHAR(50), comment='废水排放口名称')
    OUTPOINT_POSITION = Column(VARCHAR(100), comment='排放口位置')
    OUTPOINT_TYPE = Column(VARCHAR(50), comment='废气排放口类型')
    LONGITUDE = Column(DECIMAL(9, 5), comment='废气排放口经度')
    LATITUDE = Column(DECIMAL(9, 5), comment='废气排放口纬度')
    HEIGHT = Column(DECIMAL(5, 2), comment='废气排放口高度')
    WATER_AREA_CODE = Column(VARCHAR(50), comment='受纳水体功能区类别')
    RULE_CODE = Column(VARCHAR(50), comment='废水排放规律代码')
    WHERE_CODE = Column(VARCHAR(50), comment='废水排放去向代码')
    WSYSTEM_CODE = Column(VARCHAR(50), comment='受纳水体代码')
    ATTRIBUTE_CODE = Column(VARCHAR(50), comment='排口属性')
    NET_CODE = Column(VARCHAR(50), comment='接纳管网代码')
    SEWAGE_COMP_CODE = Column(VARCHAR(50), comment='排入污水处理厂代码')
    SEWAGE_COMP_NAME = Column(VARCHAR(40), comment='排入污水处理厂名称')
    INRIVER_LONGITUDE = Column(DECIMAL(9, 6), comment='入河口经度')
    INRIVER_LATITUDE = Column(DECIMAL(9, 6), comment='入河口纬度')
    STAND = Column(VARCHAR(100), comment='水排放标准')
    STAND_CODE = Column(VARCHAR(100), comment='执行标准代码')
    CONDITION_CODE = Column(VARCHAR(50), comment='执行标准条件代码')
    OUTPOINT_STATUS = Column(VARCHAR(255), comment='排放口状态（0=正常；1=异常）')
    SYS_CREATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
