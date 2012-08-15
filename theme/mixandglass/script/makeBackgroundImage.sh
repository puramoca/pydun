#!/bin/bash

# It is totally up to this script to produce icon for given category - whether
# it'll copy existing one or use any graphic tool to do so, we don't care. 

# Result must be in ${PYD_DST_BCKGR_IMAGE}

env | sort | grep PYD >> /tmp/ttt
echo " " >> /tmp/ttt

cp "${PYD_SRC_BCKGR_IMAGE}" "${PYD_DST_BCKGR_IMAGE}"

