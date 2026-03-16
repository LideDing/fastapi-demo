#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="fastapi-demo"
CONTAINER_NAME="fastapi-demo"
PORT="${APP_PORT:-8000}"
ENV_FILE="${ENV_FILE:-.env}"

# Check for .env file
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found."
    echo ""
    echo "Create one from the template:"
    echo "  cp .env.example .env"
    echo "  # then edit .env with your values"
    exit 1
fi

# Stop existing container if running
podman rm -f "$CONTAINER_NAME" 2>/dev/null || true

# Build image
echo "Building image: $IMAGE_NAME ..."
podman build -t "$IMAGE_NAME" .

# Run container
echo "Starting container: $CONTAINER_NAME on port $PORT ..."
podman run -d \
    --name "$CONTAINER_NAME" \
    --env-file "$ENV_FILE" \
    -p "$PORT:8000" \
    "$IMAGE_NAME"

echo ""
echo "Container started. Access the app at http://127.0.0.1:$PORT"
echo ""
echo "Useful commands:"
echo "  podman logs -f $CONTAINER_NAME    # view logs"
echo "  podman stop $CONTAINER_NAME       # stop"
echo "  podman rm $CONTAINER_NAME         # remove"
