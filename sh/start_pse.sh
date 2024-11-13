#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/usr/local/runJar/spider-core/project
export JOBPATH=/usr/local/runJar/spider-core/project
export PYTHON3PATH=/opt/python3/bin/python3

## $1:(1=zz;2=ls)
## $2:枣庄(1=公司；2=排口；3=废气；4=废气VOC；) 崂山(1=公司；2=排口；3=废气；5=废水；6=污水厂；7=自行监测数据)
## $3:(-d=时间类型(1=小时；2=天；3=月；4=年))

##枣庄
if [ $1 == "zz" ]; then
  if [ $2 == 1 ]; then
      echo "Start run zz_company.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/pse/zz_company.py >>${JOBPATH}/logs/zz_company.log 2>&1 &
  fi
  if [ $2 == 2 ]; then
      echo "Start run zz_outlet.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/pse/zz_outlet.py >>${JOBPATH}/logs/zz_outlet.log 2>&1 &
  fi
  if [ $2 == 3 ]; then
      echo "Start run monitor_gas.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/pse/zz_monitor_gas.py -d $3 >>${JOBPATH}/logs/zz_monitor_gas.log 2>&1 &
  fi
  if [ $2 == 4 ]; then
      echo "Start run monitor_gas_vocs.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/pse/zz_monitor_gas_vocs.py -d $3 >>${JOBPATH}/logs/zz_monitor_gas_vocs.log 2>&1 &
  fi
fi
##崂山
if [ $1 == "ls" ]; then
  if [ $2 == 1 ]; then
      echo "Start run ls_company.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/pse/ls_company.py >>${JOBPATH}/logs/ls_company.log 2>&1 &
  fi
  if [ $2 == 2 ]; then
      echo "Start run ls_outlet.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/pse/ls_outlet.py >>${JOBPATH}/logs/ls_outlet.log 2>&1 &
  fi
  if [ $2 == 3 ]; then
      echo "Start run ls_monitor_gas.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/pse/ls_monitor_gas.py -d $3 >>${JOBPATH}/logs/ls_monitor_gas.log 2>&1 &
  fi
  if [ $2 == 5 ]; then
      echo "Start run ls_monitor_water.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/pse/ls_monitor_water.py  -d $3 >>${JOBPATH}/logs/ls_monitor_water.log 2>&1 &
  fi
  if [ $2 == 6 ]; then
      echo "Start run ls_monitor_water_bus.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/pse/ls_monitor_water_bus.py  -d $3 >>${JOBPATH}/logs/ls_monitor_water_bus.log 2>&1 &
  fi
  if [ $2 == 7 ]; then
      echo "Start run ls_monitor_gas_inspect.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/pse/ls_monitor_gas_inspect.py  -d $3 >>${JOBPATH}/logs/ls_monitor_gas_inspect.log 2>&1 &
  fi
fi

##/var/spool/cron/
## crontab -e
##zz-废气
#20 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 3 1
#5 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 3 2
#5 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 3 3
#5 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 3 4
##zz-废气voc
#21 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 4 1
#10 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 4 2
#10 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 4 3
#10 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh zz 4 4
##ls-废气
#22 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 3 1
#15 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 3 2
#15 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 3 3
#15 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 3 4
##ls-废水
#24 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 5 1
#20 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 5 2
#20 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 5 3
#20 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 5 4
##ls-污水厂
#25 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 6 1
#25 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 6 2
#25 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 6 3
#25 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 6 4
##ls-自行监测
#26 * * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 7 1
#30 8 * * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 7 2
#30 3 */3 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 7 3
#30 4 */10 * * sh /usr/local/runJar/spider-core/sh/start_pse.sh ls 7 4

