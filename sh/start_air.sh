#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/usr/local/runJar/spider-core/project
export JOBPATH=/usr/local/runJar/spider-core/project
export PYTHON3PATH=/opt/python3/bin/python3

## $1:(1=zz;2=ls)
## $2:枣庄(1=；) 崂山(1=出租车走航路段)

##枣庄
if [ $1 == "zz" ]; then
  if [ $2 == 1 ]; then
      echo "Start run test.py !"
  fi
fi
##崂山
if [ $1 == "ls" ]; then
  if [ $2 == 1 ]; then
      echo "Start run taxiSailing.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/air/taxiSailing.py -dn $3 >>${JOBPATH}/logs/taxiSailing.log 2>&1 &
  fi
  if [ $2 == 2 ]; then
      echo "Start run catering.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/air/catering.py -d $3 >>${JOBPATH}/logs/catering.log 2>&1 &
  fi
  if [ $2 == 3 ]; then
      echo "Start run catering.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/air/catering.py -d $3 >>${JOBPATH}/logs/catering.log 2>&1 &
  fi
  if [ $2 == 4 ]; then
      echo "Start run ls_slagcar_record.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/air/ls_slagcar_record.py >>${JOBPATH}/logs/ls_slagcar_record.log 2>&1 &
  fi
  if [ $2 == 5 ]; then
      echo "Start run ls_catering_data.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/air/ls_catering_data.py -d $1 >>${JOBPATH}/logs/ls_catering_data.log 2>&1 &
  fi
  if [ $2 == 5 ]; then
      echo "Start run ls_catering_data.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/air/ls_catering_data.py -d $2 >>${JOBPATH}/logs/ls_catering_data.log 2>&1 &
  fi
  if [ $2 == 5 ]; then
      echo "Start run ls_catering_data.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/air/ls_catering_data.py -d $3 >>${JOBPATH}/logs/ls_catering_data.log 2>&1 &
  fi
fi

##/var/spool/cron/
## crontab -e
##ls-出租车走航
#30 8 * * * sh /usr/local/runJar/spider-core/sh/start_air.sh ls 1
##ls-餐饮分钟数据
#*/10 * * * * sh /usr/local/runJar/spider-core/sh/start_air.sh ls 2 1
##餐饮超标
#0 0 0/1 * * ? sh /usr/local/runJar/spider-core/sh/start_air.sh ls 3 2