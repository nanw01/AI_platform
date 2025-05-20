# Check execution policy
$currentPolicy = Get-ExecutionPolicy
if ($currentPolicy -eq "Restricted") {
    Write-Host "Current execution policy is Restricted. Need to change it to RemoteSigned." -ForegroundColor Yellow
    Write-Host "Do you want to change execution policy? (Y/N)" -ForegroundColor Yellow
    $answer = Read-Host
    if ($answer -eq "Y" -or $answer -eq "y") {
        Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
        Write-Host "Execution policy changed to RemoteSigned." -ForegroundColor Green
    }
    else {
        Write-Host "Canceled. Script will exit." -ForegroundColor Red
        exit
    }
}

# Check if Docker is installed and running
try {
    $dockerVersion = docker --version
    Write-Host "Docker detected: $dockerVersion" -ForegroundColor Green
    
    $dockerInfo = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "Docker not found or not running. Please install and start Docker first." -ForegroundColor Red
    exit 1
}

# 检查必要文件
$requiredFiles = @(
    "orchestrator/requirements.txt",
    "api/gateway/requirements.txt"
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "Missing required file: $file" -ForegroundColor Red
        exit 1
    }
}

# Display welcome message
Write-Host "`nWelcome to AI Microservices Platform" -ForegroundColor Cyan
Write-Host "Select an operation:" -ForegroundColor Cyan
Write-Host "1. Start API Gateway only" -ForegroundColor Yellow
Write-Host "2. Start all services" -ForegroundColor Yellow
Write-Host "3. Stop all services" -ForegroundColor Yellow
Write-Host "4. Rebuild and start all services" -ForegroundColor Yellow
Write-Host "5. View logs" -ForegroundColor Yellow
Write-Host "6. Exit" -ForegroundColor Yellow

$option = Read-Host "Enter option (1-6)"

switch ($option) {
    "1" {
        Write-Host "Starting API Gateway..." -ForegroundColor Cyan
        docker-compose up api-gateway
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to start API Gateway. Check error messages." -ForegroundColor Red
            exit 1
        }
    }
    "2" {
        Write-Host "Starting all services..." -ForegroundColor Cyan
        docker-compose up -d
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to start services. Check error messages." -ForegroundColor Red
            exit 1
        }
        Write-Host "All services started successfully." -ForegroundColor Green
        Write-Host "API Gateway URL: http://localhost:8000" -ForegroundColor Green
    }
    "3" {
        Write-Host "Stopping all services..." -ForegroundColor Cyan
        docker-compose down
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to stop services. Check error messages." -ForegroundColor Red
            exit 1
        }
        Write-Host "All services stopped." -ForegroundColor Green
    }
    "4" {
        Write-Host "Rebuilding and starting all services..." -ForegroundColor Cyan
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to rebuild and start services. Check error messages." -ForegroundColor Red
            exit 1
        }
        Write-Host "All services rebuilt and started successfully." -ForegroundColor Green
        Write-Host "API Gateway URL: http://localhost:8000" -ForegroundColor Green
    }
    "5" {
        Write-Host "Viewing logs..." -ForegroundColor Cyan
        docker-compose logs -f
    }
    "6" {
        Write-Host "Exiting..." -ForegroundColor Cyan
        exit 0
    }
    default {
        Write-Host "Invalid option. Please enter a number between 1-6." -ForegroundColor Red
        exit 1
    }
} 