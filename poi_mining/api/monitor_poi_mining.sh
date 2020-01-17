#!/bin/bash

while true;do
    procnum=` ps -ef|grep "server.py"|grep -v grep|wc -l`
    if [ $procnum -eq 0  ]; then
        echo "restart"
        #`python send_mail.py "poi_mining warning" "Warning:The poi_mining server has been restarted on gss05"`
        `python server.py &`
    fi
    sleep 2
done
