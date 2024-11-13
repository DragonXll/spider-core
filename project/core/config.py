from pydantic import BaseSettings
import os


class SystemSettings(BaseSettings):
    # 数据源配置
    MYSQL_URI: str = 'mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/ls_env_cloud?charset=utf8mb4'
    MYSQL_ECHO: bool = True

class Settings(BaseSettings):
    # 数据源配置
    MYSQL_URI: str = 'mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_base?charset=utf8mb4'
    MYSQL_ECHO: bool = True

# sqlacodegen mysql://root:Xizheng123!@192.168.110.157:3306/dc_env_base --tables t_pub_company_pse > PubCompanyPse.py

class AirSettings(BaseSettings):
    # 数据源配置
    MYSQL_URI: str = 'mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_air?charset=utf8mb4'
    MYSQL_ECHO: bool = True

class PseSettings(BaseSettings):
    # 数据源配置
    MYSQL_URI: str = 'mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_pse?charset=utf8mb4'
    MYSQL_ECHO: bool = True


class CemSettings(BaseSettings):
    # 数据源配置
    MYSQL_URI: str = 'mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_cem?charset=utf8mb4'
    MYSQL_ECHO: bool = True

class EmergencySettings(BaseSettings):
    # 数据源配置
    MYSQL_URI: str = 'mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_ecological?charset=utf8mb4'
    MYSQL_ECHO: bool = True

class SoilSettings(BaseSettings):
    # 数据源配置
    MYSQL_URI: str = 'mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_soil?charset=utf8mb4'
    MYSQL_ECHO: bool = True
class WaterSettings(BaseSettings):
    # 数据源配置
    MYSQL_URI: str = 'mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_water?charset=utf8mb4'
    MYSQL_ECHO: bool = True

system_settings = SystemSettings()
settings = Settings()
air_settings = AirSettings()
pse_settings = PseSettings()
emergency_settings = EmergencySettings()
cem_settings = CemSettings()
soil_settings = SoilSettings()
water_settings = WaterSettings()

air_config_info = {
    'host': '192.168.110.157',
    'port': 3306,
    'user': 'root',
    'passwd': 'Xizheng123!',
    'db': 'dc_env_air',
    'charset': 'utf8'
}
base_config_info = {
    'host': '192.168.110.157',
    'port': 3306,
    'user': 'root',
    'passwd': 'Xizheng123!',
    'db': 'dc_env_base',
    'charset': 'utf8'
}
hsw_config_info = {
    'host': '192.168.110.157',
    'port': 3306,
    'user': 'root',
    'passwd': 'Xizheng123!',
    'db': 'dc_env_hsw',
    'charset': 'utf8'
}
