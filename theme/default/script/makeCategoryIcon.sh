#!/bin/bash

# It is totally up to this script to produce icon for given category - whether
# it'll copy existing one or use any graphic tool to do so, we don't care. 

# Result must be in ${PYD_CATEGORY_DIRPATH}/${PYD_ICON_CAT_FILE}
#PYD_CATEGORY_NAME="I"
#PYD_ICON_CATEGORY_WIDTH=377
#PYD_ICON_CATEGORY_HEIGHT=233
#PYD_CATEGORY_DIRPATH=.
#PYD_ICON_FILE=icon.jpg
#PYD_ICON_SEL_FILE=icon_sel.jpg

# Set fonts, horizontal offset etc
FONTPATH=/usr/share/fonts/TTF/liberation
FONTRG=${FONTPATH}/LiberationSans-Regular.ttf
FONTBD=${FONTPATH}/LiberationSans-Bold.ttf
FONTIT=${FONTPATH}/LiberationSans-Italic.ttf
BORDER=17
# Compression option for PNG images
#COMPRESSOPT="-define png:compression-level=0"
COMPRESSOPT="-quality 02"
SMWIDTH=`echo "${PYD_ICON_CATEGORY_WIDTH}-${BORDER}" | bc -l`
SMWIDTH2=`echo "${PYD_ICON_CATEGORY_WIDTH}-${BORDER}*2" | bc -l`
SMHEIGHT=`echo "${PYD_ICON_CATEGORY_HEIGHT}-${BORDER}" | bc -l`
SMHEIGHT2=`echo "${PYD_ICON_CATEGORY_HEIGHT}-${BORDER}*2" | bc -l`
CANVAS1=${TMP:-/tmp}/pydun_canvas1.png
TMPCANVAS2=${TMP:-/tmp}/pydun_canvas2.png
TMPCANVAS3=${TMP:-/tmp}/pydun_canvas3.png
TMPCANVAS4=${TMP:-/tmp}/pydun_canvas4.png
CAT_NAME_LEN=${#PYD_CATEGORY_NAME}
COLOUR1=grey
COLOUR2=maroon

if [ ${CAT_NAME_LEN} -eq 1 ]; then
    # Larger font for titles
    FONTSIZE=72
    FONT=${FONTBD}
else
    FONTSIZE=44
    FONT=${FONTRG}
fi

# Get translation strings for categories
if [ -f "${PYD_LOCALE_DIR}/${PYD_LANG}.sh" ]; then
  . "${PYD_LOCALE_DIR}/${PYD_LANG}.sh"
else
  # Default to English
  . "${PYD_LOCALE_DIR}/en.sh"
fi

if [ ! -z ${TRANSLATED} ]; then
  arr=("${TRANSLATED[@]}")
  for ix in ${!arr[*]}
  do
	TRANSKEY="${arr[$ix]%#*}"
	TRANSVAL="${arr[$ix]#*#}"
	if [ "${PYD_CATEGORY_NAME}" == "${TRANSKEY}" ]; then
	  PYD_CATEGORY_NAME="${TRANSVAL}"
	  break
	fi
  done
fi


# Make icon
convert -size ${PYD_ICON_CATEGORY_WIDTH}x${PYD_ICON_CATEGORY_HEIGHT} \
    ${COMPRESSOPT} canvas:${COLOUR1} ${CANVAS1}
convert -size ${SMWIDTH}x${SMHEIGHT} ${COMPRESSOPT} canvas:${COLOUR2} ${TMPCANVAS2} 
convert -size ${SMWIDTH2}x${SMHEIGHT2} -pointsize ${FONTSIZE} -background ${COLOUR2} \
    -font "${FONT}" ${COMPRESSOPT} \
    -fill ${COLOUR1} -gravity Center caption:"${PYD_CATEGORY_NAME}" ${TMPCANVAS3}
composite -gravity center ${TMPCANVAS3} ${TMPCANVAS2} ${TMPCANVAS4}
composite -gravity center ${TMPCANVAS4} ${CANVAS1} "${PYD_CATEGORY_DIRPATH}"/${PYD_ICON_CAT_FILE}

# Make "selected" icon by inverting colours
convert -size ${PYD_ICON_CATEGORY_WIDTH}x${PYD_ICON_CATEGORY_HEIGHT} \
    ${COMPRESSOPT} canvas:${COLOUR2} ${CANVAS1}
convert -size ${SMWIDTH}x${SMHEIGHT} ${COMPRESSOPT} canvas:${COLOUR1} ${TMPCANVAS2} 
convert -size ${SMWIDTH2}x${SMHEIGHT2} -pointsize ${FONTSIZE} -background ${COLOUR1} \
    -font "${FONT}" ${COMPRESSOPT} \
    -fill ${COLOUR2} -gravity Center caption:"${PYD_CATEGORY_NAME}" ${TMPCANVAS3}
composite -gravity center ${TMPCANVAS3} ${TMPCANVAS2} ${TMPCANVAS4}
composite -gravity center ${TMPCANVAS4} ${CANVAS1} "${PYD_CATEGORY_DIRPATH}"/${PYD_ICON_CAT_SEL_FILE}

rm -f ${CANVAS1} ${TMPCANVAS2} ${TMPCANVAS3} ${TMPCANVAS4}
