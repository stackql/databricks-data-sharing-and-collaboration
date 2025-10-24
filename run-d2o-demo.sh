#!/bin/bash
# Bash script to run D2O Delta Sharing demo in Docker
# This script builds and runs a Docker container with Jupyter Lab for demonstrating D2O Delta Sharing

echo "========================================"
echo "D2O Delta Sharing Demo - Docker Setup"
echo "========================================"
echo ""

# Check if Docker is running
echo "Checking Docker..."
if ! docker version &> /dev/null; then
    echo "Error: Docker is not running. Please start Docker."
    exit 1
fi
echo "✓ Docker is running"

# Check if config.share exists
CONFIG_PATH="$(dirname "$0")/.creds/config.share"
if [ ! -f "$CONFIG_PATH" ]; then
    echo "Error: config.share not found at: $CONFIG_PATH"
    echo "Please run the provider notebook first to generate the credential file."
    exit 1
fi
echo "✓ Found config.share"

# Read the config.share content
CONFIG_CONTENT=$(cat "$CONFIG_PATH")
echo "✓ Loaded credentials"

# Build the Docker image
echo ""
echo "Building Docker image..."
docker build -t d2o-delta-sharing-demo .
if [ $? -ne 0 ]; then
    echo "Error: Failed to build Docker image."
    exit 1
fi
echo "✓ Docker image built successfully"

# Stop and remove existing container if it exists
echo ""
echo "Cleaning up existing containers..."
docker stop d2o-demo 2>/dev/null
docker rm d2o-demo 2>/dev/null
echo "✓ Cleanup complete"

# Get the absolute path to the external_jupyter_notebooks directory
NOTEBOOKS_PATH="$(cd "$(dirname "$0")/external_jupyter_notebooks" && pwd)"

# Run the Docker container
echo ""
echo "Starting Docker container..."
docker run -d \
    --name d2o-demo \
    -p 8888:8888 \
    -e DELTA_SHARING_CONFIG="$CONFIG_CONTENT" \
    -v "${NOTEBOOKS_PATH}:/workspace" \
    d2o-delta-sharing-demo

if [ $? -ne 0 ]; then
    echo "Error: Failed to start Docker container."
    exit 1
fi

echo "✓ Container started successfully"

# Wait a moment for Jupyter to start
echo ""
echo "Waiting for Jupyter Lab to start..."
sleep 3

echo ""
echo "========================================"
echo "SUCCESS! Container is running"
echo "========================================"
echo ""
echo "Jupyter Lab is accessible at:"
echo "  http://localhost:8888"
echo ""
echo "The notebook 'd2o_example.ipynb' is available in the workspace."
echo ""
echo "To view container logs:"
echo "  docker logs d2o-demo"
echo ""
echo "To stop the container:"
echo "  docker stop d2o-demo"
echo ""
echo "To remove the container:"
echo "  docker rm d2o-demo"
echo ""
