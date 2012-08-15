#!/bin/bash

# It is totally up to this script to produce icon for given episode - whether
# it'll copy existing one or use any graphic tool to do so, we don't care. 

# Result must be in ${PYD_PART_THUMB}

# Uncomment for testing
#PYD_BCKGR_IMAGE=warty_final_ubuntu_2-wallpaper-1920x1080.jpg
#PYD_CAT_DUFO_TPL=/home/zoli/project/python/pydis/template/dune_folder_category_template.txt
#PYD_CATEGORY_DIRPATH=/tmp/pydis/Year/Last_Year
#PYD_CATEGORY="Last Year"
#PYD_CATEGORY_NAME="Last Year"
#PYD_DST_BCKGR_IMAGE="/tmp/pydis/Library/Game Of Thrones S01E01 - Winter Is Coming/background.jpg"
#PYD_DST_THUMB_IMAGE="/tmp/pydis/Library/Game Of Thrones S01E01 - Winter Is Coming/icon.aai"
#PYD_ICON_FILE=icon.aai
#PYD_ICON_HEIGHT=233
#PYD_ICON_LARGE_FILE=icon_large.jpg
#PYD_ICON_SCALE_FACTOR=0.8
#PYD_ICON_SEL_FILE=icon_sel.aai
#PYD_ICON_USE_SEL=True
#PYD_ICON_WIDTH=377
#PYD_IMAGE_DIR=/home/zoli/project/python/pydis/image
#PYD_LOG_FILE=/tmp/PYDIS.log
#PYD_MOV_ACODEC=MP3
#PYD_MOV_ACTORS="Peter Dinklage, Kit Harington, Emilia Clarke, Richard Madden, Maisie Williams, Aidan Gillen, Michelle Fairley, Lena Headey, Elyes Gabel, Nonso Anozie, Oona Chaplin, Kate Dickie, Peter Vaughan, Patrick Malahide, Rose Leslie, Charles Dance, Natalia Tena, Julian Glover, Joe Dempsie, Tom Wlaschiha, Finn Jones, Kristian Nairn, Donald Sumpter, Sibel Kekilli, John Bradley, Esmé Bianco, Gethin Anthony, Natalie Dormer, Jerome Flynn, Gwendoline Christie, Gemma Whelan, Liam Cunningham, Carice van Houten, Stephen Dillane, Conleth Hill, Sophie Turner, Rory McCann, Mark Addy, Jack Gleeson, Iain Glen, Alfie Allen, Harry Lloyd, Isaac Hempstead-Wright, Jason Momoa, Nikolaj Coster-Waldau, Sean Bean"
#PYD_MOV_ASPECT=1.777:1
#PYD_MOV_CERT=TV-MA
#PYD_MOV_COMPANY=HBO
#PYD_MOV_COUNTRY=
#PYD_MOV_DIRECTORS="Tim Van Patten"
#PYD_MOV_FPS=23.976
#PYD_MOVIE_DUFO_TPL=/home/zoli/project/python/pydis/template/dune_folder_movie_template.txt
#PYD_MOVIESET_DUFO_TPL=/home/zoli/project/python/pydis/template/dune_folder_movieset_template.txt
#PYD_MOV_LANG=English
#PYD_MOV_ORIG_TITLE="Game of Thrones"
#PYD_MOV_OUTLINE=
#PYD_MOV_PART=1
#PYD_MOV_PLOT="Based on the fantasy novel series 'A Song of Ice and Fire,' Game of Thrones explores the story of an epic battle among seven kingdoms and two ruling families in the only game that matters - the Game of Thrones. All seek control of the Iron Throne, the possession of which ensures survival through the 40-year winter to come."
#PYD_MOV_QUOTE=
#PYD_MOV_RELEASE_DATE=2011-04-17
#PYD_MOV_RUNTIME=
#PYD_MOV_SUBTITLES=Serbian
#PYD_MOV_TAGLINE=
#PYD_MOV_TITLE="Игра престола"
#PYD_MOV_VCODEC=XviD
#PYD_MOV_WRITERS="David Benioff, D. B. Weiss"
#PYD_MOV_YEAR=2011
#PYD_OUT_DIR=/tmp/pydis
#PYD_PART_AIRED=2011-04-17
#PYD_PART_PLOT="A Night’s Watch deserter is tracked down outside of Winterfell, prompting swift justice by Lord Eddard “Ned” Stark and raising concerns about the dangers in the lawless lands north of the Wall. Returning home, Ned learns from his wife Catelyn that his mentor, Jon Arryn, has died in the Westeros capital of King’s Landing, and that King Robert is on his way north to offer Ned Arryn’s position as the King’s Hand. Meanwhile, across the Narrow Sea in Pentos, Viserys Targaryen hatches a plan to..."
#PYD_PART_THUMB="/tmp/pydis/Library/Game Of Thrones S01E01 - Winter Is Coming/icon_part01.jpg"
#PYD_PART_TITLE="Зима долази"
#PYD_PART_VIDIMG="/digital/yamj/Jukebox/Game Of Thrones S01E01 - Winter Is Coming.videoimage.jpg"
#PYD_SCRIPTS_DIR=/home/zoli/project/python/pydis/script
#PYD_SRC_BCKGR_IMAGE="/digital/yamj/Jukebox/Game Of Thrones S01E01 - Winter Is Coming.background.jpg"
#PYD_SRC_THUMB_IMAGE="/digital/yamj/Jukebox/Game Of Thrones S01E01 - Winter Is Coming_small.jpg"
#PYD_SUBCAT_DUFO_TPL=/home/zoli/project/python/pydis/template/dune_folder_subcategory_template.txt
#PYD_TL_DUFO_TPL=/home/zoli/project/python/pydis/template/dune_folder_toplevel_template.txt
#PYD_TPL_DIR=/home/zoli/project/python/pydis/template
#PYD_TVSET_DUFO_TPL=/home/zoli/project/python/pydis/template/dune_folder_tvset_template.txt
#PYD_YAMJ_DIR=/digital/yamj/Jukebox

touch "${PYD_PART_THUMB}"
exit 0

# Total height of picture
TOTALHEIGHT=220
# Total width in picture, in pixels
TOTALWIDTH=1700
PARTWIDTH=`echo "${TOTALHEIGHT}-20" | bc -l`
PLOTWIDTH=1120
VIDIMGWIDTH=`echo "${TOTALWIDTH}-${PLOTWIDTH}-${PARTWIDTH}" | bc -l`
NOIMAGE=0
# Border between video image and text, in pixels
BORDERWITH=20
LESSBORDER=`echo "${PLOTWIDTH}-${BORDERWITH}" | bc -l`
HALFBORDERWIDTH=`echo "scale=0; ${BORDERWITH} / 2" | bc -l`
PLOTHEIGHT=`echo "${TOTALHEIGHT}-${HALFBORDERWIDTH}-50" | bc -l`

PLOTLENGTH=${#PYD_PART_PLOT}
if [ ${PLOTLENGTH} -gt 350 ]; then
    CUTOFPLOT="${PYD_PART_PLOT:0:350} ..."
else
    CUTOFPLOT=${PYD_PART_PLOT}
fi

# Make image displaying movie part
convert -background black -fill yellow -size ${PARTWIDTH}x${TOTALHEIGHT} \
    -pointsize 140 -gravity center label:"${PYD_MOV_PART}" moviepart.png

# Create soft edge around video image
if [ ! -z "${PYD_PART_VIDIMG}" ]; then
    if [ -f "${PYD_PART_VIDIMG}" ]; then
        convert -trim -resize ${VIDIMGWIDTH}x${TOTALHEIGHT} "${PYD_PART_VIDIMG}" -virtual-pixel transparent \
            -channel A -blur 0x8 -level 50%,100% +channel soft_edge.png
        # Remove transparency
        convert soft_edge.png -background black -alpha remove -alpha off soft_edge.jpg
    else
        NOIMAGE=1
    fi
else
    NOIMAGE=1
fi

if [ $NOIMAGE -eq 1 ]; then
    convert -size ${VIDIMGWIDTH}x${TOTALHEIGHT} -background black -gravity center \
        -fill grey caption:"No image available" -virtual-pixel transparent \
        -channel A -blur 0x8 -level 50%,100% +channel soft_edge.png
    convert soft_edge.png -background black -alpha remove -alpha off soft_edge.jpg
fi

# Create label and caption with part title and plot
convert -background black -fill yellow -gravity West -size ${LESSBORDER}x50 \
    label:"${PYD_PART_TITLE}" titlemovie1.png
convert \( titlemovie1.png -background black -gravity SouthWest -splice ${BORDERWITH}x${HALFBORDERWIDTH} \) \
    titlemovie2.png

convert -background black -fill white -gravity NorthWest -size ${LESSBORDER}x${PLOTHEIGHT} \
    caption:"${CUTOFPLOT}" plotmovie1.png
convert \( plotmovie1.png -background black -gravity West -splice ${BORDERWITH}x0 \) \
    plotmovie2.png

# Put them all together
convert \( moviepart.png soft_edge.jpg +append \) \
        \( titlemovie2.png plotmovie2.png -append \) \
        +append "${PYD_PART_THUMB}"
        
rm -f moviepart*.png soft_edge.??g titlemovie*.png plotmovie*.png 
exit 0
