@echo off
chcp 65001 > nul
cd /d "E:\wild_web_program_python"
call conda activate paddle
echo 欢迎使用野山参等级分类系统！
start "" "http://127.0.0.1:5000"
python app.py