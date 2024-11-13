# coding: utf-8
from sqlalchemy import BigInteger, Column, Index, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TPubCompanyTag(Base):
    __tablename__ = 't_pub_company_tag'
    __table_args__ = (
        Index('index', 'CREDIT_NO', 'SYS_CITY_CODE', 'SYS_COUNTY_CODE', 'TAG_NAME', unique=True),
        {'comment': '企业_标签'}
    )

    ID = Column(BigInteger, primary_key=True, comment='主键')
    CREDIT_NO = Column(VARCHAR(255), comment='营业执照(统一信用代码)')
    TAG_NAME = Column(VARCHAR(255), comment='标签\\n')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
    SYS_CREATE_TIME = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    IS_DELETE = Column(BigInteger, server_default=text("'0'"), comment='是否删除0生效1失效')
