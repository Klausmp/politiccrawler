#!/bin/bash
# deploy_jenkins.sh

# Load local environment variables from .env
source .env

# Ensure the required variable is set (e.g., JENKINS_HOST)
if [ -z "$JENKINS_HOST" ]; then
  echo "JENKINS_HOST is not set in .env. Aborting."
  exit 1
fi

# Use REMOTE_TMP_DIR from environment if set; otherwise, default to ./jenkins
REMOTE_TMP_DIR="${REMOTE_TMP_DIR:-./jenkins}"

echo "Deploying to host: $JENKINS_HOST"
echo "Ensuring remote directory '$REMOTE_TMP_DIR' exists on $JENKINS_HOST..."

# Create remote directory
ssh "$JENKINS_HOST" "mkdir -p $REMOTE_TMP_DIR"

# Copy the docker-compose file from the local directory to the remote directory
echo "Copying docker-compose.yml to remote host..."
scp ./docker/jenkins/docker-compose.yml "$JENKINS_HOST:$REMOTE_TMP_DIR"

# Sanitize .env file by removing lines starting with YT_API_KEY= or DATABASE_URL=
echo "Sanitizing .env file..."
sed '/^YT_API_KEY=/d; /^DATABASE_URL=/d' .env > .env.sanitized

# Copy the sanitized .env file to the remote directory as .env
echo "Copying sanitized .env file to remote host..."
scp .env.sanitized "$JENKINS_HOST:$REMOTE_TMP_DIR/.env"

# Clean up the temporary file locally
rm .env.sanitized

# Deploy on the remote host using Docker Compose v2
echo "Deploying services on remote host using docker compose..."
ssh "$JENKINS_HOST" <<'EOF'
REMOTE_TMP_DIR="./jenkins"
# Ensure the remote directory exists
mkdir -p "$REMOTE_TMP_DIR"
cd "$REMOTE_TMP_DIR"
pwd
ls -a
# Source the .env file to load environment variables
source .env
# Check if "docker compose" is available; if not, install the plugin
if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose not found. Installing docker-compose-plugin..."
  sudo apt-get update && sudo apt-get install -y docker-compose-plugin
fi
# Start services using Docker Compose v2
docker compose up -d --remove-orphans
EOF

echo "Deployment complete!"
