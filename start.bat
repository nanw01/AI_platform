@echo off
echo =====================================
echo   启动AI微服务平台
echo =====================================

echo 请选择启动选项:
echo 1. 仅启动API网关 (构建无缓存)
echo 2. 启动全部服务 (构建无缓存)
echo 3. 仅启动API网关 (使用缓存)
echo 4. 启动全部服务 (使用缓存)

set /p option=请输入选项 (1-4): 

if "%option%"=="1" (
    echo 正在重新构建api-gateway (无缓存模式)...
    docker-compose build --no-cache api-gateway
    if %ERRORLEVEL% NEQ 0 (
        echo api-gateway 构建失败
        pause
        exit /b 1
    )
    echo 构建成功，正在启动api-gateway服务...
    docker-compose up api-gateway
) else if "%option%"=="2" (
    echo 正在重新构建所有服务 (无缓存模式)...
    docker-compose build --no-cache
    if %ERRORLEVEL% NEQ 0 (
        echo 服务构建失败
        pause
        exit /b 1
    )
    echo 构建成功，正在启动所有服务...
    docker-compose up
) else if "%option%"=="3" (
    echo 正在构建api-gateway (使用缓存)...
    docker-compose build api-gateway
    if %ERRORLEVEL% NEQ 0 (
        echo api-gateway 构建失败
        pause
        exit /b 1
    )
    echo 构建成功，正在启动api-gateway服务...
    docker-compose up api-gateway
) else if "%option%"=="4" (
    echo 正在构建所有服务 (使用缓存)...
    docker-compose build
    if %ERRORLEVEL% NEQ 0 (
        echo 服务构建失败
        pause
        exit /b 1
    )
    echo 构建成功，正在启动所有服务...
    docker-compose up
) else (
    echo 无效选项，请重新运行脚本并选择 1-4 之间的数字
    pause
    exit /b 1
)

if %ERRORLEVEL% NEQ 0 (
    echo 服务启动失败，请检查错误信息
    pause
    exit /b 1
)

pause 