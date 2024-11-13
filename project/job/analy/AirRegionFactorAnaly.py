# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from database.mysql import get_air_db
import numpy as np

qua = [0, 50, 100, 150, 200, 300, 400, 500]
# 小时AQI计算中需要用到的Idata
Idata = [
    [0, 35, 75, 115, 150, 250, 350, 500],  # PM2.5 24小时平均
    [0, 50, 150, 250, 350, 420, 500, 600],  # （PM10）24小时平均
    [0, 150, 500, 650, 800],  # so2
    [0, 100, 200, 700, 1200, 2340, 3090, 3840],  # no2
    [0, 5, 10, 35, 60, 90, 120, 150],  # co
    [0, 160, 200, 300, 400, 800, 1000, 1200]  # o3
]
# 上为24hAQI计算中需要用到的Idata
# Idata = [
#     [0, 35, 75, 115, 150, 250, 350, 500],  # PM2.5
#     [0, 50, 150, 250, 350, 420, 500, 600],  # （PM10）
#     [0, 50, 150, 475, 800, 1600, 2100, 2620],  # (SO2)
#     [0, 40, 80, 180, 280, 565, 750, 940],  # no2
#     [0, 2, 4, 14, 24, 36, 48, 60],  # （CO）
#     [0, 100, 160, 215, 265, 800]  # (O3)
# ]
dataKeyList = ['PM₂.₅', 'PM₁₀', 'SO₂', 'NO₂', 'CO', 'O₃']
dataIKeyList = ['IPM₂.₅', 'IPM₁₀', 'ISO₂', 'INO₂', 'ICO', 'IO₃']

## AQI计算、计算AQI级别
def calcAqi(airDataLine):
    IAQI = list(np.zeros(1))
    T_IA = 0
    i = j = k = 0
    I_param_map ={};
    primarypollutant =''
    for i in range(len(Idata)):
        T_data = airDataLine[:, i]
        T_Idata = Idata[i]
        for j in range(len(T_data)):
            for k in range(1, len(T_Idata)):
                if T_Idata[k] > T_data[j]:
                    break
            if k == (len(T_Idata) - 1) and T_Idata[k] < T_data[j]:
                T_IA = T_Idata[k]
            else:
                T_IA = int(round((((qua[k] - qua[k - 1]) / (T_Idata[k] - T_Idata[k - 1])) * (
                            T_data[j] - T_Idata[k - 1]) + qua[k - 1]) + 0.5))
            I_param_map[dataIKeyList[i]]=T_IA
            if T_IA > IAQI[j]:
                IAQI[j] = T_IA
                primarypollutant=dataKeyList[i]
            # elif T_IA == IAQI[j]:
            #     print(dataKeyList[i])

    if IAQI[0] <=50:
        primarypollutant = "无";
    result = {};
    result['aqi'] = IAQI[0]
    result["primarypollutant"] = primarypollutant;
    result['I_param_map'] = I_param_map
    result['quality_param'] = getLevel(result['aqi'])

    return result

## 计算AQI级别
def getLevel(aqi):
    quality_param ={}
    float(aqi)
    quality = "";
    if (aqi=='') :
        quality_param['AQISTATIONNAME'] = "无"
        quality_param['AQILEVELNAME'] = "无"
        quality_param['CODE_AQILEVEL'] = "无"
    else:
        if (aqi <= 0.0) :
            quality_param['AQISTATIONNAME']  = "无"
            quality_param['AQILEVELNAME'] = "无"
            quality_param['CODE_AQILEVEL'] = "无"
        elif (aqi <= 50.0):
            quality_param['AQILEVELNAME']  = "优"
            quality_param['AQISTATIONNAME'] = "一级"
            quality_param['CODE_AQILEVEL'] = "Ⅰ"
        elif (aqi <= 100.0) :
            quality_param['AQILEVELNAME']  = "良"
            quality_param['AQISTATIONNAME'] = "二级"
            quality_param['CODE_AQILEVEL'] = "Ⅱ"
        elif (aqi <= 150.0) :
            quality_param['AQILEVELNAME']  = "轻度污染"
            quality_param['AQISTATIONNAME'] = "三级"
            quality_param['CODE_AQILEVEL'] = "Ⅲ"
        elif (aqi <= 200.0) :
            quality_param['AQILEVELNAME']  = "中度污染"
            quality_param['AQISTATIONNAME'] = "四级"
            quality_param['CODE_AQILEVEL'] = "Ⅳ"
        elif (aqi <= 300.0) :
            quality_param['AQILEVELNAME']  = "重度污染"
            quality_param['AQISTATIONNAME'] = "五级"
            quality_param['CODE_AQILEVEL'] = "Ⅴ"
        else :
            quality_param['AQILEVELNAME']  = "严重污染"
            quality_param['AQISTATIONNAME'] = "六级"
            quality_param['CODE_AQILEVEL'] = "Ⅵ"
        return quality_param;
def analy():
    air_db: Session = next(get_air_db())

    ## 1-获取空气质量数据
    outLat = air_db.execute("""
        SELECT id,REGION_CODE,REGION_NAME,MONITOR_TIME,SO2,NO2,PM10,CO,O3,PM2_5,SYS_CITY_CODE,SYS_COUNTY_CODE
         FROM t_air_region_hour where MONITOR_TIME>DATE_SUB(NOW(), INTERVAL 3 hour) 
        """).all()
    air_db.commit()

    print("------update size ：" + str(len(outLat)) + "------")
    for out in outLat:
        print('out：', out)

        ## 2-计算AQI、首污、AQI级别
        if (out[4] == '' or out[5] == '' or out[6] == ''
                or out[7] == '' or out[8] == '' or out[9] == ''
                or out[4] == None or out[5] == None or out[6] == None
                or out[7] == None or out[8] == None or out[9] == None
            ):
            continue
        airDataLine = np.array(
            [float(out[9]), float(out[6]), float(out[4]), float(out[5]),
             float(out[7]), float(out[8])]).reshape(1, 6)
        print(airDataLine)
        result = calcAqi(airDataLine)


        # print(result)
        ## 3-修改空气质量数据
        update_sql = "update t_air_region_hour set " \
                     + "aqi=" + str(result['aqi']) \
                     + ",PRIMARY_POLLUTANT='" + str(result['primarypollutant']) \
                     + "',IPM2_5=" + str(result['I_param_map']['IPM₂.₅']) \
                     + ",IPM10=" + str(result['I_param_map']['IPM₁₀']) \
                     + ",ISO2=" + str(result['I_param_map']['ISO₂']) \
                     + ",INO2=" + str(result['I_param_map']['INO₂']) \
                     + ",ICO=" + str(result['I_param_map']['ICO']) \
                     + ",IO3=" + str(result['I_param_map']['IO₃']) \
                     + ",AQI_STATION_NAME='" + str(result['quality_param']['AQISTATIONNAME']) + "'" \
                     + ",AQI_LEVEL_NAME='" + str(result['quality_param']['AQILEVELNAME']) + "'" \
                     + ",AQI_LEVEL_CODE='" + str(result['quality_param']['CODE_AQILEVEL']) + "'" \
                     + " where POINT_CODE='" + str(out[1]) + "' and MONITOR_TIME='" + str(
            out[3]) + "'"
        print(update_sql)
        outLat = air_db.execute(update_sql)
        air_db.commit()
    air_db.close()

if __name__ == '__main__':
    global bean, creditNo
    print("---------------------------analy data start------------------------------")
    analy()
    print("---------------------------analy data end------------------------------")

