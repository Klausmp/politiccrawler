#!/bin/bash

echo "Running build_jenkins.sh..."
./scripts/build_jenkins.sh || { echo "Build failed. Aborting deployment."; exit 1; }

echo "Running remote_deploy_jenkins.sh..."
./scripts/remote_deploy_jenkins.sh || { echo "Remote deployment failed."; exit 1; }

echo "Both scripts ran successfully."
