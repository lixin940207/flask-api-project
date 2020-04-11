#!/usr/bin/env bash
tag_suffix=$1
SCRIPTS_DIR=$(cd `dirname $0`; pwd)
PROJECT_DIR=$(cd $(dirname ${SCRIPTS_DIR}); pwd)
cd "${PROJECT_DIR}"
pwd

tag="prod_${tag_suffix:-"latest"}"
echo "image tag: ${tag}"

docker build -f scripts/Dockerfile.prod -t dockerhub.datagrand.com/nlp_platform/nlp_platform_api_v2:${tag} .
docker push dockerhub.datagrand.com/nlp_platform/nlp_platform_api_v2:${tag}
