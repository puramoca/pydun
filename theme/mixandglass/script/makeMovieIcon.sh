#!/bin/sh

if [ -z "${PYD_SRC_ICON_IMAGE}" -o -z "${PYD_DST_ICON_IMAGE}" -o -z ${PYD_ICON_WIDTH} -o -z ${PYD_ICON_HEIGHT} ]; then
  exit 1
fi

# Take current dimensions - maybe icon is correct size?
CURR_ICON_WIDTH=`identify -format "%[fx:w]" "${PYD_SRC_ICON_IMAGE}"`
CURR_ICON_HEIGHT=`identify -format "%[fx:h]" "${PYD_SRC_ICON_IMAGE}"`

# Maybe we tried to identify dimensions of a directory or some other filesystem object?
if [ -z ${CURR_ICON_WIDTH} -o -z ${CURR_ICON_HEIGHT} ]; then
  exit 1
fi

if [ ${PYD_ICON_WIDTH} -eq ${CURR_ICON_WIDTH} -a ${PYD_ICON_HEIGHT} -eq ${CURR_ICON_HEIGHT} ]; then
  # Rare case, but possible if using default icon (which is hopefully right dimensions)
  # "de facto", not just "de iure"
  exit 0
fi

convert "${PYD_SRC_ICON_IMAGE}" -resize ${PYD_ICON_WIDTH} r1
NEWHEIGHT=`identify -format "%[fx:h]" r1`
Y=`echo "scale=0; (${NEWHEIGHT}-${PYD_ICON_HEIGHT}) / 2" | bc -l`

if [ ${Y} -gt 0 ]; then
  convert r1 -crop "${PYD_ICON_WIDTH}x${PYD_ICON_HEIGHT}+0+${Y}" r2
else
  convert "${PYD_SRC_ICON_IMAGE}" -resize ${PYD_ICON_WIDTH}x${PYD_ICON_HEIGHT} r2
fi

# If there's appropriate mask with round corners, apply it
ROUND_MASK="${PYD_IMAGE_DIR}"/round_corner_mask_${PYD_ICON_WIDTH}x${PYD_ICON_HEIGHT}.png

if [ -f "${ROUND_MASK}" ]; then
  convert r2 -alpha Set "${ROUND_MASK}" \
    \( -clone 0,1 -alpha Opaque -compose Hardlight -composite \) \
    -delete 0 -compose In -composite "${PYD_DST_ICON_IMAGE}"
else
  cp -f r2 "${PYD_DST_ICON_IMAGE}"
fi

rm -f r1 r2
