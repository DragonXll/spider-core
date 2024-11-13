#!/bin/bash
export PYTHONPATH=$PYTHONPATH:/usr/local/runJar/spider-core/project
export JOBPATH=/usr/local/runJar/spider-core/project
export PYTHON3PATH=/opt/python3/bin/python3


##崂山

echo "Start run ls_elec.py !"
${PYTHON3PATH} ${JOBPATH}/job/elec/ls_elec.py >>${JOBPATH}/logs/ls_elec.log 2>&1 &




##/var/spool/cron/
## crontab -e
##zz-废气
#0 16 * * * sh /usr/local/runJar/spider-core/sh/start_elec.sh