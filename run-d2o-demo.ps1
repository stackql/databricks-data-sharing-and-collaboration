# PowerShell script to run D2O Delta Sharing demo in Docker
# This script builds and runs a Docker container with Jupyter Lab for demonstrating D2O Delta Sharing

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "D2O Delta Sharing Demo - Docker Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $null = docker version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Docker is running" -ForegroundColor Green
}
catch {
    Write-Host "Error: Docker is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

# Check if config.share exists
$configPath = Join-Path $PSScriptRoot ".creds\config.share"
if (-not (Test-Path $configPath)) {
    Write-Host "Error: config.share not found at: $configPath" -ForegroundColor Red
    Write-Host "Please run the provider notebook first to generate the credential file." -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Found config.share" -ForegroundColor Green

# Read the config.share content
$configContent = Get-Content $configPath -Raw
Write-Host "✓ Loaded credentials" -ForegroundColor Green

# Build the Docker image
Write-Host ""
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build -t d2o-delta-sharing-demo .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to build Docker image." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Docker image built successfully" -ForegroundColor Green

# Stop and remove existing container if it exists
Write-Host ""
Write-Host "Cleaning up existing containers..." -ForegroundColor Yellow
docker stop d2o-demo 2>$null
docker rm d2o-demo 2>$null
Write-Host "✓ Cleanup complete" -ForegroundColor Green

# Get the absolute path to the external_jupyter_notebooks directory
$notebooksPath = Join-Path $PSScriptRoot "external_jupyter_notebooks"

# Run the Docker container
Write-Host ""
Write-Host "Starting Docker container..." -ForegroundColor Yellow
docker run -d `
    --name d2o-demo `
    -p 8888:8888 `
    -e DELTA_SHARING_CONFIG="$configContent" `
    -v "${notebooksPath}:/workspace" `
    d2o-delta-sharing-demo

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to start Docker container." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Container started successfully" -ForegroundColor Green

# Wait a moment for Jupyter to start
Write-Host ""
Write-Host "Waiting for Jupyter Lab to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SUCCESS! Container is running" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Jupyter Lab is accessible at:" -ForegroundColor Cyan
Write-Host "  http://localhost:8888" -ForegroundColor White
Write-Host ""
Write-Host "The notebook 'd2o_example.ipynb' is available in the workspace." -ForegroundColor Cyan
Write-Host ""
Write-Host "To view container logs:" -ForegroundColor Yellow
Write-Host "  docker logs d2o-demo" -ForegroundColor White
Write-Host ""
Write-Host "To stop the container:" -ForegroundColor Yellow
Write-Host "  docker stop d2o-demo" -ForegroundColor White
Write-Host ""
Write-Host "To remove the container:" -ForegroundColor Yellow
Write-Host "  docker rm d2o-demo" -ForegroundColor White
Write-Host ""
