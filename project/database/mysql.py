from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import system_settings, soil_settings
from core.config import settings
from core.config import air_settings
from core.config import pse_settings
from core.config import cem_settings
from core.config import emergency_settings
from core.config import water_settings
from core.logger import logger

from mod import Base

system_engine = create_engine(
    url=system_settings.MYSQL_URI,
    echo=system_settings.MYSQL_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    pool_recycle=3600,
    isolation_level='READ UNCOMMITTED'
)
engine = create_engine(
    url=settings.MYSQL_URI,
    echo=settings.MYSQL_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    pool_recycle=3600,
    isolation_level='READ UNCOMMITTED'
)

air_engine = create_engine(
    url=air_settings.MYSQL_URI,
    echo=air_settings.MYSQL_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    pool_recycle=3600,
    isolation_level='READ UNCOMMITTED'
)

pse_engine = create_engine(
    url=pse_settings.MYSQL_URI,
    echo=pse_settings.MYSQL_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    pool_recycle=3600,
    isolation_level='READ UNCOMMITTED'
)
emergency_engine = create_engine(
    url=emergency_settings.MYSQL_URI,
    echo=emergency_settings.MYSQL_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    pool_recycle=3600,
    isolation_level='READ UNCOMMITTED'
)
cem_engine = create_engine(
    url=cem_settings.MYSQL_URI,
    echo=cem_settings.MYSQL_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    pool_recycle=3600,
    isolation_level='READ UNCOMMITTED'
)

soil_engine = create_engine(
    url=soil_settings.MYSQL_URI,
    echo=soil_settings.MYSQL_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    pool_recycle=3600,
    isolation_level='READ UNCOMMITTED'
)
water_engine = create_engine(
    url=water_settings.MYSQL_URI,
    echo=water_settings.MYSQL_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    pool_recycle=3600,
    isolation_level='READ UNCOMMITTED'
)

system_localSession = sessionmaker(
    bind=system_engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False
)
localSession = sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False
)

air_localSession = sessionmaker(
    bind=air_engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False
)

pse_localSession = sessionmaker(
    bind=pse_engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False
)


emergency_localSession = sessionmaker(
    bind=emergency_engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False
)

cem_localSession = sessionmaker(
    bind=cem_engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False
)

soil_localSession = sessionmaker(
    bind=soil_engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False
)
water_localSession = sessionmaker(
    bind=water_engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False
)

def get_soil_db():
    try:
        db = soil_localSession()
        yield db
    except Exception as e:
        logger.error(f'获取数据库失败 -- 失败信息如下:\n{e}')
    finally:
        db.close()

def get_pse_db():
    try:
        db = pse_localSession()
        yield db
    except Exception as e:
        logger.error(f'获取数据库失败 -- 失败信息如下:\n{e}')
    finally:
        db.close()


def get_system_db():
    try:
        db = system_localSession()
        yield db
    except Exception as e:
        logger.error(f'获取数据库失败 -- 失败信息如下:\n{e}')
    finally:
        db.close()

def get_db():
    try:
        db = localSession()
        yield db
    except Exception as e:
        logger.error(f'获取数据库失败 -- 失败信息如下:\n{e}')
    finally:
        db.close()

def get_db_emergency():
    try:
        db = emergency_localSession()
        yield db
    except Exception as e:
        logger.error(f'获取数据库失败 -- 失败信息如下:\n{e}')
    finally:
        db.close()

def get_air_db():
    try:
        db = air_localSession()
        yield db
    except Exception as e:
        logger.error(f'获取数据库失败 -- 失败信息如下:\n{e}')
    finally:
        db.close()

def get_pse_db():
    try:
        db = pse_localSession()
        yield db
    except Exception as e:
        logger.error(f'获取数据库失败 -- 失败信息如下:\n{e}')
    finally:
        db.close()

def get_cem_db():
    try:
        db = cem_localSession()
        yield db
    except Exception as e:
        logger.error(f'获取数据库失败 -- 失败信息如下:\n{e}')
    finally:
        db.close()


def create_db():
    try:
        Base.metadata.create_all(engine)
        logger.success('表结构加载完成')
    except Exception as e:
        logger.error(f'表结构加载失败 -- 错误信息如下:\n{e}')
    finally:
        engine.dispose()


def drop_db():
    try:
        Base.metadata.drop_all(engine)
        logger.success('表结构删除完成')
    except Exception as e:
        logger.error(f'表结构删除失败 -- 错误信息如下:\n{e}')
    finally:
        engine.dispose()

def get_water_db():
    try:
        db = water_localSession()
        yield db
    except Exception as e:
        logger.error(f'获取数据库失败 -- 失败信息如下:\n{e}')
    finally:
        db.close()

def init_db():
    drop_db()
    create_db()
