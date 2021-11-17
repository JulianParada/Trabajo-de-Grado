@echo off

REM set PythonDIR=.\Python\Python39\
REM set PATH=%PythonDIR%;%PythonDIR%\Scripts;%PATH%
REM set PYTHONPATH=%PythonDIR%\Lib;%PythonDIR%\Lib\site-packages;%PythonDIR%\DLLs;
REM set PATHEXT=%PATHEXT%;.PY;.PYW

REM assoc .py=Python.File>NUL
REM assoc .pyw=PythonW.File>NUL
REM ftype Python.File="%PythonDIR%\python.exe" %%1 %%*>NUL
REM ftype PythonW.File="%PythonDIR%\pythonw.exe" %%1 %%*>NUL

set OSF_PASSWORD=7245piapiado
osf -p 7urpa -u julian_parada@javeriana.edu.co clone ../OSFDocuments/informestecnicos
REM osf -p y5673 -u julian_parada@javeriana.edu.co clone C:/Users/estudiante/Documents/OSFDocuments/informestecnicos2
osf -p jrgp8 -u julian_parada@javeriana.edu.co clone ../OSFDocuments/pofi

exit