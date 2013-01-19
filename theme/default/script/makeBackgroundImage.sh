#!/bin/bash
 
# It is totally up to this script to produce background for given movie - whether
# it'll copy existing one or use any graphic tool to do so, we don't care. 

# Result must be in file pointed to by ${PYD_DST_BCKGR_IMAGE}

# Testing remnants
#echo "# Environment dumped by script $0" >> /tmp/Movie_env_vars.sh
#env | sort | grep PYD >> /tmp/Movie_env_vars.sh
#echo " " >> /tmp/Movie_env_vars.sh

. ../../../test/BourneIdentity.sh

genrectlbl()
{
	subtxt="$1"
	subheight="$2"
	subbgr="$3"
	subfntsize="$4"
	subfile="$5"
	
	convert -size x${subheight} -background ${subbgr} -fill black -font ${FONTBD} \
      -gravity Center -pointsize ${subfntsize} label:" ${subtxt} " ${TMPIMG}

    convert ${TMPIMG} \
      \( +clone  -alpha extract \
        -draw 'fill black polygon 0,0 0,6 6,0 fill white circle 6,6 6,0' \
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
BGRHEIGHT=`echo $BGRSIZE | cut -d"x" -f2`
BGRWIDTH=`echo $BGRSIZE | cut -d"x" -f1`
LBLCOLOUR="cornsilk2"
# Width of text label "Directed By", "Actors" etc
LBLWIDTH=220
# y-offset from middle of the background where movie icon should be placed
ICONOFFSETY=30
IMGMOVDATA1=${TMP:-/tmp}/moviedata1.png
IMGMOVDATA2=${TMP:-/tmp}/moviedata2.png
IMGMOVDATA3=${TMP:-/tmp}/moviedata3.png
TMPIMG=${TMP:-/tmp}/pydun.png
TMPMVG=${TMP:-/tmp}/pydun.mvg
TMPFILE=${TMP:-/tmp}/labels.txt
TMPROUNDEDCORNERMASK=${TMP:-/tmp}/pydun_rounded_corner_mask.png
TMPROUNDEDCORNEROVERLAY=${TMP:-/tmp}/pydun_rounded_corner_overlay.png
TMPICON=${TMP:-/tmp}/pydun_tmp_icon.png
TMPMOVIECONT=${TMP:-/tmp}/pydun_movie_cont.png
TMPFRAMERATE=${TMP:-/tmp}/pydun_frame_rate.png
TMPMOVASPECT=${TMP:-/tmp}/pydun_movie_aspect.png
TMPVCODEC=${TMP:-/tmp}/pydun_movie_vcodec.png
TMPACODEC=${TMP:-/tmp}/pydun_movie_acodec.png

# Get common strings, regardless of language
. "${PYD_LOCALE_DIR}/common.sh"

# Get localized labels if necessery
if [ -f "${PYD_LOCALE_DIR}/${PYD_LANG}.sh" ]; then
  . "${PYD_LOCALE_DIR}/${PYD_LANG}.sh"
else
  # Default to English
  . "${PYD_LOCALE_DIR}/en.sh"
fi

# Colour for year, agency rating and duration
CLR3="yellow"
# Colour to draw plot text
CLRPLOT="white"
# Colour to draw cast
CLRCAST="grey"
# Colour to draw title
CLRTITLE="yellow"
# Colour to draw original title
CLRORIGTITLE="grey91"
# Colour to draw director's name
CLRDIRECTORS="grey"
# Colour do draw screenplay writers names
CLRSCREENPLAY="grey"
# Empty temporary file that will hold labels, texts and their coordinates
> ${TMPFILE}

# Calculate where to put movie icon, nicely centered
ICONPAGEX=`echo "scale=0; (${XOFFSET}-${PYD_ICON_WIDTH}) / 2" | bc -l`
ICONPAGEY=`echo ${BGRHEIGHT}+${ICONOFFSETY} | bc -l`

# Determine what to do based of show type - a movie or TV episode
if [ -z "${PYD_MOV_IS_TVSET}" ]; then
  # It is a movie
  if [ ! -z "${PYD_MOV_PLOT}" ]; then
	PLOTTXT="${PYD_MOV_PLOT}"
  else
    if [ ! -z "${PYD_MOV_PLOT_OUTLINE}" ]; then
	  PLOTTXT="${PYD_MOV_PLOT_OUTLINE}"
	else
	  PLOTTXT="${LBLNOPLOT}"
    fi
  fi
  cp -f "${PYD_DST_ICON_IMAGE}" ${TMPICON}
  TITLETXT="${PYD_MOV_TITLE}"
else
  # It is a TV episode
  if [ ! -z "${PYD_PART_PLOT}" ]; then
    PLOTTXT="${PYD_PART_PLOT}"
  else
    if [ ! -z "${PYD_MOV_PLOT}" ]; then
      PLOTTXT="${PYD_MOV_PLOT}"
    else
      if [ ! -z "${PYD_MOV_OUTLINE}" ]; then
        PLOTTXT="${PYD_MOV_OUTLINE}"
      else
        PLOTTXT="${LBLNOPLOT}"
      fi
    fi
  fi
  if [ ! -z "${PYD_PART_VIDIMG}" -a -f "${PYD_PART_VIDIMG}" ]; then
    # Usually videoimage needs some trimming and resizing
    convert -trim "${PYD_PART_VIDIMG}" -resize ${PYD_ICON_WIDTH}x${PYD_ICON_HEIGHT} \
      -gravity center ${TMPICON}
  else
    cp -f "${PYD_DST_ICON_IMAGE}" ${TMPICON}
  fi
  TITLETXT="${PYD_MOV_TITLE} - ${LBLEPISODEABBR} ${PYD_PART_MOV}: ${PYD_PART_TITLE}"
fi

# Use # as field separator because of possible space in path (e.g. under Windows)
echo "label 1460 west ${CLRTITLE} ${FNTTITLESIZE} ${XOFFSET} ${YOFFSET} ${FONTBD} ${TITLETXT}" >> ${TMPFILE}

# If original title differs, add it as well
if [ "${PYD_MOV_ORIG_TITLE}" != "${PYD_MOV_TITLE}" ]; then
  YOFFSET=`echo ${YOFFSET}+55 | bc -l`
  echo "label 970 west ${CLRORIGTITLE} ${FNTORIGTITLESIZE} ${XOFFSET} ${YOFFSET} ${FONTIT} ${PYD_MOV_ORIG_TITLE}" >> ${TMPFILE}
  YYEARTIMEOFFSET=70
else
  YOFFSET=`echo ${YOFFSET}+10 | bc -l`
  YYEARTIMEOFFSET=50
fi

YOFFSET=`echo ${YOFFSET}+60 | bc -l`
echo "label ${LBLWIDTH} west ${LBLCOLOUR} ${FNTDATASIZE} ${XOFFSET} ${YOFFSET} ${FONT} ${LBLSCREENPLAY}" >> ${TMPFILE}
echo "label 870 west ${CLRSCREENPLAY} ${FNTDATASIZE} ${X1OFFSET} ${YOFFSET} ${FONT} ${PYD_MOV_WRITERS}" >> ${TMPFILE}

YOFFSET=`echo ${YOFFSET}+40 | bc -l`
echo "label ${LBLWIDTH} west ${LBLCOLOUR} ${FNTDATASIZE} ${XOFFSET} ${YOFFSET} ${FONT} ${LBLDIRECTEDBY}" >> ${TMPFILE}
echo "label 870 west ${CLRDIRECTORS} ${FNTDATASIZE} ${X1OFFSET} ${YOFFSET} ${FONT} ${PYD_MOV_DIRECTORS}" >> ${TMPFILE}

YOFFSET=`echo ${YOFFSET}+40 | bc -l`
echo "label ${LBLWIDTH} west ${LBLCOLOUR} ${FNTDATASIZE} ${XOFFSET} ${YOFFSET} ${FONT} ${LBLSTUDIO}" >> ${TMPFILE}
echo "label 870 west grey ${FNTDATASIZE} ${X1OFFSET} ${YOFFSET} ${FONT} ${PYD_MOV_COMPANY}" >> ${TMPFILE}

YOFFSET=`echo ${YOFFSET}+40 | bc -l`
echo "label ${LBLWIDTH} west ${LBLCOLOUR} ${FNTDATASIZE} ${XOFFSET} ${YOFFSET} ${FONT} ${LBLCAST}" >> ${TMPFILE}
echo "caption 1270 west ${CLRCAST} ${FNTDATASIZE} ${X1OFFSET} ${YOFFSET} ${FONT} ${PYD_MOV_ACTORS:0:180}" >> ${TMPFILE}

# If we added original movie title under movie title, calculate how much to move
# plot text further down
if [ "${PYD_MOV_ORIG_TITLE}" != "${PYD_MOV_TITLE}" ]; then
  YOFFSET=`echo ${YOFFSET}+80 | bc -l`
else
  YOFFSET=`echo ${YOFFSET}+80 | bc -l`
fi
echo "caption 1460 west ${CLRPLOT} 30 ${XOFFSET} ${YOFFSET} ${FONTBD} ${PLOTTXT}" >> ${TMPFILE}

# Movie data: year, country, certificate, runtime
if [ ! -z "${PYD_MOV_COUNTRY}" ]; then
  MOVIEDATA="${PYD_MOV_YEAR} (${PYD_MOV_COUNTRY}), ${PYD_MOV_CERT}, ${PYD_MOV_RUNTIME}"
else
  MOVIEDATA="${PYD_MOV_YEAR}, ${PYD_MOV_CERT}, ${PYD_MOV_RUNTIME}"
fi
echo "label 540 east ${CLR3} ${FNTDATASIZE} ${XYEARTIMEOFFSET} ${YYEARTIMEOFFSET} ${FONT} ${MOVIEDATA}" >> ${TMPFILE}

# First add text fields
cat ${TMPFILE} |
while read typ width gravity color pointsize x y font text
do
  convert -size ${width}x -gravity ${gravity} -fill ${color} -background ${BACKGROUND} \
    -font ${font} -pointsize ${pointsize} -page +${x}+${y} ${typ}:"${text} " miff:-
done | convert -size ${BGRSIZE} -background 'rgba(0,0,0,0.40)' caption:'' - -flatten ${IMGMOVDATA1}

# Add fields that require nice rounded border

# Movie container
CNTLOW=${PYD_MOV_CONTAINER,,}
if [ -f "${PYD_IMAGE_DIR}"/"${CNTLOW}.png" ]; then
  TMPMOVIECONT="${PYD_IMAGE_DIR}"/"${CNTLOW}.png"
else
  CNT="${CONTAINERCODE[${CNTLOW}]}"
  if [ "$CNT" == "" ]; then
    CNT="${PYD_MOV_CONTAINER}"
  fi
  genrectlbl "${CNT}" 40 whitesmoke 26 ${TMPMOVIECONT}
fi

# Video codec(s)
if [ "${PYD_MOV_VCODEC}" != "" ]; then
  VLOW=${PYD_MOV_VCODEC,,}
  FOUND=0
  for codec in "DivX 3" "DivX 4" "DivX 5" DivX XviD H264 MPEG4
  do
    if [[ "${VLOW}" == *${codec,,}* ]]
    then
      genrectlbl "${codec}" 40 cornsilk 26 ${TMPVCODEC}
      FOUND=1
      break
    fi
  done
  if [ $FOUND -eq 0 ]; then
    genrectlbl "${PYD_MOV_VCODEC}" 40 cornsilk 26 ${TMPVCODEC}
  fi
else
  genrectlbl "???" 40 cornsilk 26 ${TMPVCODEC}
fi

# Audio codec
if [ "${PYD_MOV_ACODEC}" != "" ]; then
  VLOW=${PYD_MOV_ACODEC,,}
  FOUND=0
  for codec in "AAC LC-SBR" "AAC LC" AAC MP3 AC3 Vorbis
  do
    if [[ "${VLOW}" == *${codec,,}* ]]
    then
      genrectlbl "${codec}" 40 cornsilk 26 ${TMPACODEC}
      FOUND=1
      break
    fi
  done
  if [ $FOUND -eq 0 ]; then
    genrectlbl "${PYD_MOV_ACODEC}" 40 cornsilk 26 ${TMPACODEC}
  fi
else
  genrectlbl "???" 40 cornsilk 26 ${TMPACODEC}
fi

# Frame rate
genrectlbl "${PYD_MOV_FPS}" 40 WhiteSmoke 26 ${TMPFRAMERATE}

# Movie aspect
genrectlbl "${PYD_MOV_ASPECT}" 40 skyblue 26 ${TMPMOVASPECT}

oIFS="$IFS"
IFS=', '

# Audio languages
AUDIOLIST=""
read -a LANGARR <<< "${PYD_MOV_LANG}"
for ix in "${LANGARR[@]}"
do
  LNG="${LANGCODE[$ix]}"
  if [ "$LNG" != "" ]; then
    AUDIOLIST="${AUDIOLIST} ${PYD_IMAGE_DIR}/${LNG}.png"
  else
    AUDIOLIST="${AUDIOLIST} ${PYD_IMAGE_DIR}/UNK.png"
  fi
done
if [ "${AUDIOLIST}" != "" ]; then
  AUDIOLIST="${PYD_IMAGE_DIR}/audio2.png ${AUDIOLIST}"
fi

# Subtitles
SUBTLIST=""
read -a LANGARR <<< "${PYD_MOV_SUBTITLES}"
for ix in "${LANGARR[@]}"
do
  LNG="${LANGCODE[$ix]}"
  if [ "$LNG" != "" ]; then
    SUBTLIST="${SUBTLIST} ${PYD_IMAGE_DIR}/${LNG}.png"
  else
    SUBTLIST="${SUBTLIST} ${PYD_IMAGE_DIR}/UNK.png"
  fi
done
if [ "${SUBTLIST}" != "" ]; then
  SUBTLIST="${PYD_IMAGE_DIR}/gnome-subs.png ${SUBTLIST}"
fi

IFS="$oIFS"

# Combine them all into one picture
montage -label '' -tile x1 -background ${BACKGROUND} -geometry +6+0 ${TMPMOVIECONT} \
  ${PYD_IMAGE_DIR}/movie1.png ${TMPVCODEC} ${TMPFRAMERATE} ${PYD_IMAGE_DIR}/redmusicnote.png \
  ${TMPACODEC} null: ${TMPMOVASPECT} ${AUDIOLIST} ${SUBTLIST} null: ${IMGMOVDATA2}
# Get dimensions of newly generated picture because of precise final positioning
METASIZE=`identify -format "%[fx:w]x%[fx:h/2]" "${IMGMOVDATA2}"`
METAWIDTH=`echo $METASIZE | cut -d"x" -f1`
METAHEIGHT=`echo $METASIZE | cut -d"x" -f2`
METAOFFSETX=`echo ${BGRWIDTH}-${METAWIDTH}-10 | bc -l`
METAOFFSETY=`echo ${BGRHEIGHT}*2-${METAHEIGHT}-20 | bc -l`

# Finally, combine images
convert -page +0+${BGRHEIGHT} ${IMGMOVDATA1} \
  -page +${ICONPAGEX}+${ICONPAGEY} ${TMPICON} \
  -page +${METAOFFSETX}+${METAOFFSETY} ${IMGMOVDATA2} \
  +page -alpha Set -virtual-pixel transparent \
  \( "${PYD_SRC_BCKGR_IMAGE}" -alpha Set \) -insert 0 \
  -background ${BACKGROUND} -flatten "${PYD_DST_BCKGR_IMAGE}"
  
rm -f ${TMPFILE} ${IMGMOVDATA1} ${IMGMOVDATA2} ${IMGMOVDATA3} ${TMPIMG} ${TMPMVG} ${TMPICON} \
  ${TMPROUNDEDCORNERMASK} ${TMPROUNDEDCORNEROVERLAY} ${TMPMOVIECONT} ${TMPFRAMERATE} \
  ${TMPMOVASPECT} ${TMPVCODEC} ${TMPACODEC}
