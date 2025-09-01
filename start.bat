@echo off
REM 激活Conda环境
call conda activate PromptRose

REM 启动Python应用程序
python "%~dp0prompt_wheel.py"

REM 如果需要保持窗口打开（调试用），取消下面的注释

REM pause
