@echo off
echo 检查Conda环境...

where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 请先安装Conda
    pause
    exit /b 1
)

echo 创建/更新conda环境...
call conda env update -f environment.yml

echo 激活conda环境...
call conda activate trans

echo 启动应用...
streamlit run views\streamlit_ui.py

pause
