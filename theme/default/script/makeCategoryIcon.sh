#!/bin/bash

# It is totally up to this script to produce icon for given category - whether
# it'll copy existing one or use any graphic tool to do so, we don't care. 

# Result must be in ${PYD_CATEGORY_DIRPATH}/${PYD_ICON_FILE}

#PYD_BCKGR_IMAGE=warty_final_ubuntu_2-wallpaper-1920x1080.jpg
#PYD_CAT_DUFO_TPL=dune_folder_category_template.txt
#PYD_CATEGORY_DIRPATH=/tmp/pydis/Genres
#PYD_CATEGORY=Genres
#PYD_ICON_FILE=icon.jpg
#PYD_ICON_HEIGHT=200
#PYD_ICON_SEL_FILE=icon_sel.jpg
#PYD_ICON_USE_SEL=True
#PYD_ICON_WIDTH=400
#PYD_CATEGORY_NAME="Научна фантастика"
PYD_CATEGORY_NAME="Other"
#PYD_IMAGE_DIR=/home/zoli/project/python/pydis/image
#PYD_LOG_FILE=/tmp/PYDIS.log
#PYD_OUT_DIR=/tmp/pydis
#PYD_SCRIPTS_DIR=/home/zoli/project/python/pydis/script
#PYD_TL_DUFO_TPL=dune_folder_toplevel_template.txt
#PYD_TPL_DIR=/home/zoli/project/python/pydis/template
#PYD_YAMJ_DIR=/digital/yamj/Jukebox

#env | sort | grep PYD

BORDER=17
SMWIDTH=`echo "${PYD_ICON_WIDTH}-${BORDER}" | bc -l`
SMWIDTH23RDS=`echo "scale=0; ${PYD_ICON_WIDTH} * 7 / 8 " | bc -l`
SMHEIGHT=`echo "${PYD_ICON_HEIGHT}-${BORDER}" | bc -l`
CAT_NAME_LEN=${#PYD_CATEGORY_NAME}
COLOUR1=grey
COLOUR2=maroon

if [ ${CAT_NAME_LEN} -eq 1 ]; then
    # Larger font for titles
    FONTSIZE=72
else
    FONTSIZE=42
fi

# Make icon
convert -size ${PYD_ICON_WIDTH}x${PYD_ICON_HEIGHT} canvas:${COLOUR1} canvas1.png
convert -size ${SMWIDTH}x${SMHEIGHT} canvas:${COLOUR2} canvas2.png 
convert -size ${SMWIDTH}x${SMHEIGHT} -pointsize ${FONTSIZE} -background ${COLOUR2} -fill ${COLOUR1} -trim -gravity Center caption:"${PYD_CATEGORY_NAME}" canvas3.png
composite -gravity center canvas3.png canvas2.png canvastmp.png
composite -gravity center canvastmp.png canvas1.png ${PYD_CATEGORY_DIRPATH}/${PYD_ICON_FILE}

# Make "selected" icon by inverting colours
convert -size ${PYD_ICON_WIDTH}x${PYD_ICON_HEIGHT} canvas:${COLOUR2} canvas1.png
convert -size ${SMWIDTH}x${SMHEIGHT} canvas:${COLOUR1} canvas2.png 
convert -size ${SMWIDTH}x${SMHEIGHT} -pointsize ${FONTSIZE} -background ${COLOUR1} -fill ${COLOUR2} -trim -gravity Center caption:"${PYD_CATEGORY_NAME}" canvas3.png
composite -gravity center canvas3.png canvas2.png canvastmp.png
composite -gravity center canvastmp.png canvas1.png ${PYD_CATEGORY_DIRPATH}/${PYD_ICON_SEL_FILE}

rm -f canvas*.png
