#!/bin/sh

JUPYTER_PORT=${JUPYTER_PORT:-8888}
WEB_PDB_PORT=${WEB_PDB_PORT:-5555}

docker run --rm -it -v "`pwd`":/usr/src/app -e JUPYTER_PORT=${JUPYTER_PORT} -p ${JUPYTER_PORT}:${JUPYTER_PORT} -p ${WEB_PDB_PORT}:${WEB_PDB_PORT} metapyquod-dev

#IPADDRESS=docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CONTAINER_ID)

#echo Running container ${CONTAINER_ID} at address ${IPADDRESS}...
