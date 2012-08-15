#!/bin/bash -x

# It is totally up to this script to produce icon for given category - whether
# it'll copy existing one or use any graphic tool to do so, we don't care. 

# Result must be in ${PYD_CATEGORY_DIRPATH}/${PYD_ICON_FILE}
PYD_CATEGORY_NAME="Парк из доба јуре"
PYD_ICON_CATEGORY_WIDTH=377
PYD_ICON_CATEGORY_HEIGHT=233
PYD_CATEGORY_DIRPATH=.
PYD_ICON_FILE=icon.png
PYD_ICON_SEL_FILE=icon_sel.png

BORDER=17
SMWIDTH=`echo "${PYD_ICON_CATEGORY_WIDTH}-${BORDER}" | bc -l`
SMWIDTH2=`echo "${PYD_ICON_CATEGORY_WIDTH}-${BORDER}*2" | bc -l`
SMHEIGHT=`echo "${PYD_ICON_CATEGORY_HEIGHT}-${BORDER}" | bc -l`
SMHEIGHT2=`echo "${PYD_ICON_CATEGORY_HEIGHT}-${BORDER}*2" | bc -l`
CAT_NAME_LEN=${#PYD_CATEGORY_NAME}
COLOUR1=grey
COLOUR2=maroon

if [ ${CAT_NAME_LEN} -eq 1 ]; then
    # Larger font for titles
    FONTSIZE=72
else
    FONTSIZE=44
fi

# Get translation strings for categories
# TODO: Make language file parameter
if [ -f "${PYD_SCRIPTS_DIR}"/sr.sh ]; then
  . "${PYD_SCRIPTS_DIR}"/sr.sh
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
fi

# Make monochrome canvas
convert -size ${PYD_ICON_CATEGORY_WIDTH}x${PYD_ICON_CATEGORY_HEIGHT} canvas:${COLOUR1} canvas1.png

# Cut out rounded rectangles in all 4 corners
convert canvas1.png -alpha set  -compose Over -quality 100 \
  \( -size 20x20 xc:${COLOUR2} -draw "circle 20,20 20,0" \
     -write mpr:triangle  +delete \) \
  \( mpr:triangle             \) -gravity northwest -composite \
  \( mpr:triangle -flip       \) -gravity southwest -composite \
  \( mpr:triangle -flop       \) -gravity northeast -composite \
  \( mpr:triangle -rotate 180 \) -gravity southeast -composite \
  corner_cutoff.png
      
#convert -size ${SMWIDTH2}x${SMHEIGHT2} -pointsize ${FONTSIZE} -background ${COLOUR2} \
#    -fill ${COLOUR1} -gravity Center caption:"${PYD_CATEGORY_NAME}" canvas3.png

exit 0
# Make icon

convert -size ${SMWIDTH}x${SMHEIGHT} canvas:${COLOUR2} canvas2.png 

composite -gravity center canvas3.png canvas2.png canvastmp.png
composite -gravity center canvastmp.png canvas1.png "${PYD_CATEGORY_DIRPATH}"/${PYD_ICON_FILE}

# Make "selected" icon by inverting colours
convert -size ${PYD_ICON_CATEGORY_WIDTH}x${PYD_ICON_CATEGORY_HEIGHT} canvas:${COLOUR2} canvas1.png
convert -size ${SMWIDTH}x${SMHEIGHT} canvas:${COLOUR1} canvas2.png 
convert -size ${SMWIDTH2}x${SMHEIGHT2} -pointsize ${FONTSIZE} -background ${COLOUR1} \
    -fill ${COLOUR2} -gravity Center caption:"${PYD_CATEGORY_NAME}" canvas3.png
composite -gravity center canvas3.png canvas2.png canvastmp.png
composite -gravity center canvastmp.png canvas1.png "${PYD_CATEGORY_DIRPATH}"/${PYD_ICON_SEL_FILE}

rm -f canvas*.png
