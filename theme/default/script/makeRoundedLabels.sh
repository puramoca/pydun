#!/bin/bash

. /home/zoli/project/python/pydun/test/BourneIdentity.sh

# Set fonts, horizontal offset etc
FONTPATH=/usr/share/fonts/TTF/dejavu/
FONT=${FONTPATH}/DejaVuSansCondensed.ttf
FONTBD=${FONTPATH}/DejaVuSansCondensed-Bold.ttf
FONTIT=${FONTPATH}/DejaVuSansCondensed-Oblique.ttf
LBLFNTSIZE=24
LBLWIDTH=60
LBLHEIGHT=30
XYEARTIMEOFFSET=1360
YOFFSET=5
BACKGROUND=transparent
LBLCOLOUR="cornsilk2"
TMPIMG=${TMP:-/tmp}/pydun.png
PYDUN_TEST_DIR=/home/zoli/project/python/pydun/test

TMPROUNDEDCORNERMASK=${TMP:-/tmp}/pydun_rounded_corner_mask.png
TMPROUNDEDCORNEROVERLAY=${TMP:-/tmp}/pydun_rounded_corner_overlay.png
TMPICON=${TMP:-/tmp}/pydun_tmp_icon.png

# Get localized labels if necessery
if [ -f "${PYD_LOCALE_DIR}/${PYD_LANG}.sh" ]; then
  . "${PYD_LOCALE_DIR}/${PYD_LANG}.sh"
else
  # Default to English
  . "${PYD_LOCALE_DIR}/en.sh"
fi

gensqrlbl()
{
	if [ "$1" == "UNK" ]; then
	  lbltxt=" "
	else
	  lbltxt=$1
	fi
	lblfile=$1
	
	convert -size ${LBLWIDTH}x${LBLHEIGHT} -background ${LBLCOLOUR} -fill black -font ${FONTBD} \
      -gravity Center -pointsize ${LBLFNTSIZE} label:"${lbltxt}" +depth miff:- | \
    convert - \( +clone  -alpha extract \
        -draw 'fill black polygon 0,0 0,6 6,0 fill white circle 6,6 6,0' \
        \( +clone -flip \) -compose Multiply -composite \
        \( +clone -flop \) -compose Multiply -composite \
      \) -alpha off -compose CopyOpacity -composite \
      +depth miff:- | convert - -background none ${PYD_IMAGE_DIR}/${lblfile}.png
}

# Make labels for languages
for lang in SRB ENG HRV FRA ZHO DEU GER BOS RON FIN NLD BUL CES DAN HEB ARA HUN POR FIL SLK SLV SPA TUR TGL UNK POL NOR SWE
do
  gensqrlbl ${lang}
done

## Make labels that require same height
#genrectlbl AVI avi

# Resize some other pictures

for pic in 3ivx aac ac3 ac3+ audio avc avi-2 avi avi2 bdav blu-ray divx dts dvd flac matroska
do
  if [ -f ${PYDUN_TEST_DIR}/"${pic}".png ]; then
    convert ${PYDUN_TEST_DIR}/"${pic}".png -resize x50 -background none ${PYD_IMAGE_DIR}/"${pic}".png
  fi
done

rm -f ${TMPIMG}
