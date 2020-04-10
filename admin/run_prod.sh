#!/usr/bin/env bash
SCRIPTS_DIR=$(cd `dirname $0`; pwd)
PROJECT_DIR=$(cd $(dirname ${SCRIPTS_DIR}); pwd)
cd "${PROJECT_DIR}"
pwd

export PYTHONPATH=$(pwd)
export FLASK_APP=start_server.py
export FLASK_ENV=production
export FLASK_DEBUG=0

cd app && flask db migrate && flask db upgrade

if [ "$?" != "0" ]; then
    echo "An error occurred when flask db migrate or upgrade"
    exit 1
fi

cd ..

gunicorn start_server:app -c gunicorn_conf.py --reload
