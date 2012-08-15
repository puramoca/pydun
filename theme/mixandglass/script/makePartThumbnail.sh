#!/bin/bash

# It is totally up to this script to produce icon for given movie part - whether
# it'll copy existing one or use any graphic tool to do so, we don't care. 

# Result must be in ${PYD_PART_THUMB}

# Uncomment for testing
#PYD_PART_THUMB=icon_part1.jpg
#PYD_MOV_PART=1

COLOUR1=lightblue
COLOUR2=black
DIMENSION=80
POINTSIZE=72

# Make image displaying movie part

convert -background ${COLOUR1} -fill ${COLOUR2} -size ${DIMENSION}x${DIMENSION} \
    -pointsize ${POINTSIZE} -gravity center label:${PYD_PART_MOV} "${PYD_PART_THUMB}"

if [ ! -z "${PYD_PART_SEL_THUMB}" ]; then
    convert -background ${COLOUR2} -fill ${COLOUR1} -size ${DIMENSION}x${DIMENSION}\
        -pointsize ${POINTSIZE} -gravity center label:${PYD_PART_MOV} "${PYD_PART_SEL_THUMB}"
fi

# Clean up after yourself
rm -f bubble_overlay.png

