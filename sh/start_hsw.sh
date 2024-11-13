#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/usr/local/runJar/spider-core/project
export JOBPATH=/usr/local/runJar/spider-core/project
export PYTHON3PATH=c

## $1:(1=zz;2=ls)
## $2:枣庄(1=；) 崂山(1=出租车走航路段)
##崂山
if [ $1 == "ls" ]; then
  if [ $2 == 1 ]; then
      echo "Start run WastelessCity.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/hsw/WastelessCity.py -d $3 >>${JOBPATH}/logs/WastelessCity.log 2>&1 &
  fi
  if [ $2 == 2 ]; then
      echo "Start run Approved.py !"
      ${PYTHON3PATH} ${JOBPATH}/job/hsw/Approved.py -d $3 >>${JOBPATH}/logs/Approved.log 2>&1 &
  fi
fi

##/var/spool/cron/
## crontab -e
#危固废联单
#0 * * * * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 1 1
#0 * * * * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 1 2
#0 * * * * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 1 3
#危固废经营报告
#0 0 1 * * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 2 1
#0 0 1 1 * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 2 2
#0 0 1 1 * sh /usr/local/runJar/spider-core/sh/start_hsw.sh ls 2 3