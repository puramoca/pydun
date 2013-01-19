#!/bin/bash
 
# It is totally up to this script to produce background for given movie - whether
# it'll copy existing one or use any graphic tool to do so, we don't care. 

# Result must be in file pointed to by ${PYD_DST_BCKGR_IMAGE}

#echo "# Environment dumped by script $0" >> /tmp/Movie_env_vars.sh
#env | sort | grep PYD >> /tmp/Movie_env_vars.sh
#echo " " >> /tmp/Movie_env_vars.sh

. ./BourneIdentity.sh

set -x
genrectlbl()
{
	subtxt="$1"
	subheight="$2"
	subbgr="$3"
	subfntsize="$4"
	subfile="$5"
	
	convert -size x${subheight} -background ${subbgr} -fill black -font ${FONTBD} \
      -gravity Center -pointsize ${subfntsize} label:"${subtxt}" ${TMPIMG}

    convert ${TMPIMG} \
      \( +clone  -alpha extract \
        -draw 'fill black polygon 0,0 0,8 8,0 fill white circle 8,8 8,0' \
        \( +clone -flip \) -compose Multiply -composite \
        \( +clone -flop \) -compose Multiply -composite \
      \) -alpha off -compose CopyOpacity -composite ${subfile}
}

# Set fonts, horizontal offset etc
FONTPATH=/usr/share/fonts/TTF/liberation
FONT=${FONTPATH}/LiberationSans-Regular.ttf
FONTBD=${FONTPATH}/LiberationSans-Bold.ttf
FONTIT=${FONTPATH}/LiberationSans-Italic.ttf
# Font size for writing movie title
FNTTITLESIZE=44
# Font size for writing original movie title
FNTORIGTITLESIZE=34
# Font size for plot text
FNTPLOTSIZE=26
# Font size for writing directors, actors etc.
FNTDATASIZE=30
# X-offset of all labels: movie title, directors, actors etc.
XOFFSET=400
# X-offset of movie metadata itself
X1OFFSET=610
XYEARTIMEOFFSET=1360
YOFFSET=5
BACKGROUND=transparent
BGRSIZE=`identify -format "%[fx:w]x%[fx:h/2]" "${PYD_SRC_BCKGR_IMAGE}"`
LBLCOLOUR="cornsilk2"
# Width of text label "Directed By", "Actors" etc
LBLWIDTH=220
IMGMOVDATA1=${TMP:-/tmp}/moviedata1.png
IMGMOVDATA2=${TMP:-/tmp}/moviedata2.png
TMPIMG=${TMP:-/tmp}/pydun.png
TMPMVG=${TMP:-/tmp}/pydun.mvg
TMPFILE=${TMP:-/tmp}/labels.txt
TMPROUNDEDCORNERMASK=${TMP:-/tmp}/pydun_rounded_corner_mask.png
TMPROUNDEDCORNEROVERLAY=${TMP:-/tmp}/pydun_rounded_corner_overlay.png
TMPICON=${TMP:-/tmp}/pydun_tmp_icon.png
TMPMOVIECONT=${TMP:-/tmp}/pydun_movie_cont.png
TMPFRAMERATE=${TMP:-/tmp}/pydun_frame_rate.png
TMPMOVASPECT=${TMP:-/tmp}/pydun_movie_aspect.png

# Get common strings, regardless of language
. "${PYD_LOCALE_DIR}/common.sh"

# Get localized labels if necessery
if [ -f "${PYD_LOCALE_DIR}/${PYD_LANG}.sh" ]; then
  . "${PYD_LOCALE_DIR}/${PYD_LANG}.sh"
else
  # Default to English
  . "${PYD_LOCALE_DIR}/en.sh"
fi

genrectlbl "♫" 40 none 36 /tmp/note.png

