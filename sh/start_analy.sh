#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/usr/local/runJar/spider-core/project
export JOBPATH=/usr/local/runJar/spider-core/project
export PYTHON3PATH=/opt/python3/bin/python3

## $1:(1=大气站点AQI计算;2=大气行政区AQI计算)
if [ $1 == 1 ]; then
    echo "Start run AirPointFactorAnaly.py !"
    ${PYTHON3PATH} ${JOBPATH}/job/analy/AirPointFactorAnaly.py >>${JOBPATH}/logs/AirPointFactorAnaly.log 2>&1 &
fi
if [ $1 == 2 ]; then
    echo "Start run AirRegionFactorAnaly.py !"
    ${PYTHON3PATH} ${JOBPATH}/job/analy/AirRegionFactorAnaly.py >>${JOBPATH}/logs/AirRegionFactorAnaly.log 2>&1 &
fi


##/var/spool/cron/
## crontab -e
##大气站点AQI计算
#10/30 * * * * sh /usr/local/runJar/spider-core/sh/start_analy.sh 1
##大气行政区AQI计算
#10/30 * * * * sh /usr/local/runJar/spider-core/sh/start_analy.sh 2
