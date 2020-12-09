@echo off

if defined JUPYTER_PORT (
set _JUPYTER_PORT=%JUPYTER_PORT%
)else (
set _JUPYTER_PORT=8888
)
if defined WEB_PDB_PORT (
set _WEB_PDB_PORT=%WEB_PDB_PORT%
)else (
set _WEB_PDB_PORT=8888
)

docker run --rm -it -v "%CD%":/usr/src/app -e JUPYTER_PORT=%_JUPYTER_PORT% -p %_JUPYTER_PORT%:%_JUPYTER_PORT% -p %_WEB_PDB_PORT%:5555 sphtkr/metapyquod-dev:python3.8
