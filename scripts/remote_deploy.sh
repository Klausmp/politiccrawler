#!/bin/bash
# remote_deploy.sh

# Load local environment variables from .env
source .env

# Ensure the required variable is set (e.g., HOST)
if [ -z "$HOST" ]; then
  echo "HOST is not set in .env. Aborting."
  exit 1
fi

# Use REMOTE_HOST_TMP_DIR from environment if set; otherwise, default to ./politcrawler
REMOTE_HOST_TMP_DIR="${REMOTE_HOST_TMP_DIR:-./politcrawler}"

echo "Deploying to host: $HOST"
echo "Ensuring remote directory '$REMOTE_HOST_TMP_DIR' exists on $HOST..."

# Create the remote directory
ssh "$HOST" "mkdir -p $REMOTE_HOST_TMP_DIR"

# Copy the docker-compose file from the local directory to the remote directory
echo "Copying docker-compose.yml to remote host..."
scp ./docker-compose.yml "$HOST:$REMOTE_HOST_TMP_DIR"


# Sanitize .env file by removing lines starting with YT_API_KEY=
echo "Sanitizing .env file..."
sed '/^YT_API_KEY=/d' .env > .env.sanitized

# Copy the sanitized .env file to the remote directory as .env
echo "Copying sanitized .env file to remote host..."
scp .env.sanitized "$HOST:$REMOTE_HOST_TMP_DIR/.env"

# Clean up the temporary file locally
rm .env.sanitized

# Deploy on the remote host using Docker Compose v2
echo "Deploying services on remote host using docker compose..."
ssh "$HOST" <<'EOF'
REMOTE_HOST_TMP_DIR="./politcrawler"
# Ensure the remote directory exists (again, just to be safe)
mkdir -p "$REMOTE_HOST_TMP_DIR"
cd "$REMOTE_HOST_TMP_DIR"
# Source the .env file to load environment variables
source .env

# Check if "docker compose" is available; if not, install the plugin
if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose not found. Installing docker-compose-plugin..."
  sudo apt-get update && sudo apt-get install -y docker-compose-plugin
fi
# Start services using Docker Compose v2
docker compose up -d
EOF

echo "Deployment complete!"
