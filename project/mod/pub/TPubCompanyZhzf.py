# coding: utf-8
from sqlalchemy import BigInteger, Column, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TPubCompanyZhzf(Base):
    __tablename__ = 't_pub_company_zhzf'
    __table_args__ = (
        Index('index_uni', 'CREDIT_NO', 'SYS_CITY_CODE', 'SYS_COUNTY_CODE', unique=True),
        {'comment': '企业_执法源'}
    )

    ID = Column(BigInteger, primary_key=True, comment='ID')
    CREDIT_NO = Column(VARCHAR(64), comment='统一社会信用代码【MD5】')
    COMPANY_NAME = Column(VARCHAR(100), comment='企业名称')
    PSE_CATE = Column(String(50), comment='污染源类别')
    SYS_CREATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
