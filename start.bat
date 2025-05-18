@echo off
echo =====================================
echo   启动AI微服务平台
echo =====================================

echo 正在构建和启动服务...
docker-compose up

if %ERRORLEVEL% NEQ 0 (
    echo 服务启动失败，请检查错误信息
    pause
    exit /b 1
)

pause 