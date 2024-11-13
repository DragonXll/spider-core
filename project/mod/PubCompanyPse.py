
from sqlalchemy import BigInteger, Column, Index, Integer, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class PubCompanyPse(Base):
    __tablename__ = 't_pub_company_pse'
    __table_args__ = (
        Index('index_uni', 'PSE_CODE', 'PSE_TYPE', 'CREDIT_NO', 'SYS_CITY_CODE', 'SYS_COUNTY_CODE', unique=True),
        {'comment': '企业_污染源'}
    )

    ID = Column(BigInteger, primary_key=True, comment='ID')
    CREDIT_NO = Column(VARCHAR(64), comment='统一社会信用代码')
    PSE_NAME = Column(VARCHAR(100), comment='污染源名称')
    PSE_CODE = Column(VARCHAR(50), comment='污染源代码')
    PSE_TYPE = Column(Integer, comment='企业类型( 1=废水；2=废气；3=废气voc；4=污水厂) （101=直排海；103=应急减排 ）')
    PSE_STATUS = Column(Integer, comment='企业状态（0=在产；1=停止排放；2=停产）')
    SYS_CREATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
