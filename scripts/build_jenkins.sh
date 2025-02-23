#!/bin/bash

source .env

BUILD_DIR=.build/jenkins

mkdir -p .build

if [ -d $BUILD_DIR ]; then
  rm -rf $BUILD_DIR
fi

cp -r ./docker/jenkins $BUILD_DIR

docker build -t "${DOCKER_USER_NAME}/${JENKINS_DOCKER_NAME}:${JENKINS_DOCKER_TAG}" "${BUILD_DIR}"

docker push "${DOCKER_USER_NAME}/${JENKINS_DOCKER_NAME}:${JENKINS_DOCKER_TAG}"


