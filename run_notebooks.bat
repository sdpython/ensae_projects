
@echo off
if "%1"=="" goto default_value:
if "%1"=="default" goto default_value:
set pythonexe=%1
goto nextn:

:default_value:
@echo ~LABEL default_value
set pythonexe=C:\PythonENSAE11\python
@echo ~SET pythonexe=C:\PythonENSAE11\python

:nextn:
@echo ~LABEL nextn
set current=%~dp0
set path=%path%;%pythonexe%;%pythonexe%\Scripts
@echo ~SET path=%path%;%pythonexe%;%pythonexe%\Scripts
@echo ~CALL jupyter-notebook --notebook-dir=_doc\notebooks --matplotlib=inline
set PYTHONPATH=%PYTHONPATH%;%current%\src;%current%\..\pyquickhelper\src;%current%\..\pyensae\src;%current%\..\pyrsslocal\src;%current%\..\pymyinstall\src
@echo ~SET PYTHONPATH=%PYTHONPATH%;%current%\src;%current%\..\pyquickhelper\src;%current%\..\pyensae\src;%current%\..\pyrsslocal\src;%current%\..\pymyinstall\src
jupyter-notebook --notebook-dir=_doc\notebooks --matplotlib=inline