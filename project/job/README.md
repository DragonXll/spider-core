## 崂山
job/pse/ls_login.py 登录验证处理
job/pse/ls_company.py  污染源企业信息
job/pse/ls_monitor_gas.py 废气监测信息
job/pse/ls_monitor_gas_inspect.py 自行监测
job/pse/ls_monitor_gas_realtime.py 废气时时数据【暂未验证】
job/pse/ls_monitor_water.py  废水监测信息
job/pse/ls_monitor_water_bus.py 污水厂监测信息
job/pse/ls_outlet.py  排口信息
## 枣庄
job/pse/zz_login.py  登录验证处理
job/pse/zz_company.py 污染源企业信息
job/pse/zz_monitor_gas.py 废气监测信息
job/pse/zz_monitor_gas_vocs.py 废气VOCS监测信息
job/pse/zz_outlet.py  排口信息

## 生成实体
sqlacodegen mysql+pymysql://user:password@host/database 执行该命令后，将会生成MySQL数据库中所有表的模型代码。
sqlacodegen mysql+pymysql://user:password@host/database --tables table name --outfile models.py
# 实体生成土壤
sqlacodegen mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_soil --tables t_land_info --outfile TLandInfo
# 实体生成遥感遥测
sqlacodegen mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_air --tables t_monitor_car --outfile TMonitorCar
sqlacodegen mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_air --tables t_monitor_remote_sense_detail --outfile TMonitorRemoteSenseDetail
sqlacodegen mysql+pymysql://root:Xizheng123!@192.168.110.157:3306/dc_env_air --tables t_monitor_exceeding_standard --outfile TMonitorExceedingStandard