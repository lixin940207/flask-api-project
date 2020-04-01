#!/usr/bin/env bash
tag_suffix=$1
SCRIPTS_DIR=$(cd `dirname $0`; pwd)
PROJECT_DIR=$(cd $(dirname ${SCRIPTS_DIR}); pwd)
cd "${PROJECT_DIR}"
pwd

cp -R ~/.ssh .ssh

tag="dev_${tag_suffix}"
echo "image tag: ${tag}"

docker build -f docker/Dockerfile -t dockerhub.datagrand.com/nlp_platform/nlp_platform_api_v2:${tag} .
#docker push dockerhub.datagrand.com/nlp_platform/nlp_platform_api_v2:${tag}
