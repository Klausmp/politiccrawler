#!/bin/bash

BUILD_DIR=".build/politrunner"

pwd

source .env

if [ -d "$BUILD_DIR" ]; then
    rm -r "$BUILD_DIR"
fi

mkdir -p "$BUILD_DIR"
mkdir -p "$BUILD_DIR/src"

if [ -d "./src" ]; then
    cp -r ./src/* "$BUILD_DIR/src"
else
    echo "Warning: Source directory './src' not found!"
    exit 1
fi

if [ -f "./requirements.txt" ]; then
    cp ./requirements.txt "$BUILD_DIR"
else
    echo "Warning: 'requirements.txt' not found!"
    exit 1
fi

if [ -d "./prisma" ]; then
    mkdir -p "$BUILD_DIR/prisma"
    cp -r ./prisma/schema.prisma "$BUILD_DIR/prisma"
else
    echo "Warning: Prisma directory './prisma' not found!"
    exit 1
fi

cp ./docker/politrunner/* "$BUILD_DIR"

docker build -t "${DOCKER_USER_NAME}/${POLITRUNNER_DOCKER_NAME}:${POLITRUNNER_DOCKER_TAG}" "${BUILD_DIR}"

docker push "${DOCKER_USER_NAME}/${POLITRUNNER_DOCKER_NAME}:${POLITRUNNER_DOCKER_TAG}"