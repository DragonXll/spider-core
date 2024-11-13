# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, Index, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TPubCompany(Base):
    __tablename__ = 't_pub_company'
    __table_args__ = (
        Index('index_uni', 'CREDIT_NO', 'SYS_CITY_CODE', 'SYS_COUNTY_CODE', 'COMPANY_NAME', unique=True),
        {'comment': '企业_基础信息'}
    )

    ID = Column(Integer, primary_key=True)
    CREDIT_NO = Column(VARCHAR(64), index=True, comment='统一社会信用代码【MD5】')
    CREDIT_NO_TRUE = Column(VARCHAR(64), comment='统一社会信用代码【真正】')
    GROUP_NO = Column(VARCHAR(50), comment='所属集团公司企业代码')
    IS_SUPER = Column(Integer, comment='是否重点企业（0=默认=否；1=是）')
    COMPANY_NAME = Column(VARCHAR(100), comment='企业名称')
    COMPANY_NAME_HISTORY = Column(VARCHAR(100), comment='曾用名')
    COMPANY_STATUS = Column(String(64), comment='企业状态（示例：存续）')
    COMPANY_TYPE = Column(String(64), comment='企业类型')
    SCOPE = Column(String(1000), comment='经营范围')
    LEGAL_NO = Column(VARCHAR(50), comment='法人证件')
    LEGAL_NAME = Column(VARCHAR(50), comment='法人代表姓名')
    ENV_CONTACTS_NAME = Column(VARCHAR(50), comment='环保联系人名称')
    ENV_CONTACTS_TEL = Column(VARCHAR(50), comment='环保联系人电话')
    ADDRESS = Column(VARCHAR(255), comment='企业详细地址')
    LONGITUDE = Column(DECIMAL(9, 6), comment='中心经度')
    LATITUDE = Column(DECIMAL(9, 6), comment='中心纬度')
    TEL = Column(VARCHAR(50), comment='电话')
    FAX = Column(VARCHAR(50), comment='企业传真')
    POSTAL_CODE = Column(VARCHAR(6), comment='企业邮政编码')
    EMAIL = Column(VARCHAR(100), comment='企业电子邮件')
    WEB_SITE = Column(VARCHAR(100), comment='企业网址')
    INDUSTRY_CODE = Column(VARCHAR(255), comment='行业类别代码总（*-*-*）')
    INDUSTRY_NAME = Column(VARCHAR(255), comment='行业名称总（*-*-*）')
    INDUSTRY_CATE_NAME = Column(VARCHAR(255), comment='行业门类')
    INDUSTRY_CATE2_NAME = Column(VARCHAR(255), comment='行业大类')
    INDUSTRY_CATE3_NAME = Column(VARCHAR(255), comment='行业中类')
    INDUSTRY_CATE4_NAME = Column(VARCHAR(255), comment='行业小类')
    QUALIFICATION = Column(VARCHAR(50), comment='单位资质')
    BUILD_DATE = Column(DateTime, comment='开业时间（建成时间）')
    STOP_DATE = Column(DateTime, comment='停业时间')
    DISTRICT_CODE = Column(VARCHAR(50), comment='所属街道')
    DISTRICT_CODE_TRUE = Column(VARCHAR(50), comment='所属街道码值')
    SYS_CREATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    SYS_UPDATE_TIME = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='修改时间')
    SYS_CITY_CODE = Column(VARCHAR(20), nullable=False, server_default=text("''"), comment='所属地级市编码（实例格式：370200000000）')
    SYS_COUNTY_CODE = Column(VARCHAR(20), server_default=text("''"), comment='所属区县编码（实例格式：370283000000）')
    SYS_CREATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='创建人')
    SYS_UPDATE_NAME = Column(VARCHAR(100), server_default=text("''"), comment='修改人')
