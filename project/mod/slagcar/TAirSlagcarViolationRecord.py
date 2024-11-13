# coding: utf-8
from sqlalchemy import Column, DateTime, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TAirSlagcarViolationRecord(Base):
    __tablename__ = 't_air_slagcar_violation_record'
    __table_args__ = (
        Index('uni_inde', 'POINT_NAME', 'CAR_NO', 'CAPTURE_TIME', unique=True),
        {'comment': '大气_渣土车_抓拍违规记录'}
    )

    ID = Column(BIGINT, primary_key=True, comment='主键')
    POINT_NAME = Column(VARCHAR(200), nullable=False, comment='监测点')
    CAR_NO = Column(VARCHAR(100), nullable=False, comment='车牌号')
    IS_RECORD = Column(TINYINT, nullable=False, comment='是否备案')
    CAR_TYPE = Column(TINYINT, nullable=False, comment='车辆类型（1=大型车；2=小型车；3=渣土车；4=疑似渣土车；5=其他）【字典】')
    CAPTURE_TIME = Column(DateTime, comment='抓拍时间、经过时间')
    ORG_NAME = Column(String(255), comment='单位名称【车辆】')
    CAR_HEAD_NO = Column(String(100), comment='车牌头号码【车辆】')
    LINKMAN = Column(String(50), comment='联系人【车辆】')
    REGION_NAME = Column(String(50), comment='所属地区【车辆】')
    AUDIT_TIME = Column(DateTime, comment='审核时间')
    VIOLATION_TYPE_CODE = Column(TINYINT, nullable=False, comment='违规类型【字典】')
    VIOLATION_TYPE_NAME = Column(String(100), comment='违规类型名称')
    VIOLATION_LEVEL = Column(TINYINT, comment='违规程度（1-5）')
    MARK_STATUS = Column(TINYINT, comment='标记状态(1=已标记)【字典】')
    LANE_NUMBER = Column(TINYINT, comment='车道号')
    ELAPSED_TIME = Column(DateTime, comment='经过时间')
    CAR_HEAD_PICTURE_PATH = Column(String(200), comment='车头照片存储路径')
    CAR_TAIL_PICTURE_PATH = Column(String(200), comment='车尾照片存储路径')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("'370200000000'"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("'370212000000'"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_TIME = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
