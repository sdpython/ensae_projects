if "%1"=="" goto default_value_python:
set pythonexe="%1"
%pythonexe% setup.py write_version
goto custom_python:

:default_value_python:
set pythonexe="C:\PythonENSAE11\python\python"
:custom_python:
%pythonexe% -u setup.py build_script
if %errorlevel% neq 0 exit /b %errorlevel%