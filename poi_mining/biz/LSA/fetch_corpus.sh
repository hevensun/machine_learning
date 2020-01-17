#!/bin/bash

set -o errtrace
set -o pipefail  # trace ERR through pipes
set -o nounset   # set -u : exit the script if you try to use an uninitialised variable
set -o errexit   # set -e : exit the script if any statement returns a non-true return value

function ExecuteSQL() {
    # performing sparkSQL by Beeline
    BEELINE="beeline -u jdbc:hive2://10.107.134.23:8000 -n liangchengming -p xxxXXXxxx"
    sqlCommand="${@:1}"
    echo "${sqlCommand}"
    ${BEELINE} -e "${sqlCommand}"
}

function categoryPoiNames() {

    day="${1}"

    dir="/app/lbs/lbs-jingpin/liangchengming/cid2poiname"
    sql="
    insert overwrite directory '${dir}'
    select name, cid2
    from   nuomi.poi_all_info
    lateral view explode(sub_catg_id_a) mytab as cid2
    where  day='${day}'
    group by name, cid2
    "

    ExecuteSQL "${sql}"
    hadoop fs -getmerge "${dir}" ./cid2poinames
    iconv -f UTF-8 -t GBK -c ./cid2pidnames > cid2pidnames.gbk
}



categoryPoiNames $(date -d'1 days ago' +'%Y%m%d')
