env_name=$1

set -o errexit
echo "Start deploy to ${env_name}."
cd $ROOT_PATH
mkdir ${env_name}_deploy && cd ${env_name}_deploy
git clone --depth=1 --single-branch -b $env_name ssh://git@git.datagrand.com:58422/$DEPLOYMENT_REPO_NAMESPACE/$DEPLOYMENT_REPO_NAME.git
cd $DEPLOYMENT_REPO_NAME
git config --local user.email "${GITLAB_USER_EMAIL}"
git config --local user.name "${GITLAB_USER_NAME}"
sed -i "s/\(dockerhub.datagrand.com\/\)\(.*\)\(\/nlp_platform_api_v2:\)\(.*\)/\1nlp_platform\3dev_$DOCKER_TAG_SUFFIX/g" docker-compose.yml
git add docker-compose.yml
git commit -m "${COMMIT_MESSAGE}"
git push

ssh -f -p 22 -4 -o "StrictHostKeyChecking no" ci_test@114.118.22.249 -L $PORT:10.120.13.94:22 -N
cmd="docker service update --image=dockerhub.datagrand.com/nlp_platform/nlp_platform_api_v2:dev_'${DOCKER_TAG_SUFFIX}' deploy${env_name}_nlp_platform_api"
echo $cmd
ssh -o "StrictHostKeyChecking no" $USER@$SERVER -p $PORT $cmd