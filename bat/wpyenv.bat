@echo off

REM 命令行参数检查
if "%1" == "" (
echo Usage: pyenv [version] [drive:]path
echo Try `pyenv --help' for more information
goto over

)  else if "%1" == "--help" (
echo Usage: pyenv [version] [drive:]path
echo.
echo 描述:
echo     使用该脚本创建指定版本的 python 虚拟环境
echo.
echo 参数列表:
echo     version    指定python版本[-2, -3]
echo     path       指定文件夹名
echo.
echo 例如:
echo     pyenv -2 test
goto over

)  else if "%2" == "" (
echo Usage: pyenv [version] [drive:]path
echo Try `pyenv --help' for more information
goto over
)

REM Python 可执行文件路径
set py2_exe=E:\tools\python\python2.7\python.exe
set py3_exe=E:\tools\python\python3\python.exe

REM Python 版本
set v2=-2
set v3=-3

REM 获取指定版本
set version=%1

REM 获取指定目录
set floder_name=%2

REM 比较版本完成环境搭建
if %version% == %v2% (
virtualenv -p %py2_exe% %floder_name%
echo Completed

) else if %version% == %v3% (
virtualenv -p %py3_exe% %floder_name%
echo Completed

) else echo 参数错误


REM 程序结束
:over

