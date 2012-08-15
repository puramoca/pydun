
import logging
import os
import shutil
import sys
import xml.sax

import pydisconf
import PydMovieParser
import PydUtil


mlogger = logging.getLogger( 'PydMovieDir' )
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel( logging.INFO )
# Set a format which is simpler for console use
consoleFormatter = logging.Formatter( pydisconf.PYD_LOG_CONSOLE_FORMAT )
consoleHandler.setFormatter( consoleFormatter )
mlogger.addHandler( consoleHandler )


class PydMovieDir:
    
    def __init__(self):
        self.movieName = None
        self.movieDir = None
        self.movieDirPath = None
        self.movieYAMJPath = None
        self.parser = xml.sax.make_parser()
        self.mprs = PydMovieParser.PydMovieParser()
        self.parser.setContentHandler( self.mprs )
        self.movie = None
        self.duneFolderFile = None
        self.dfIndex = 0
        self.itemList = []

    
    # Remove all environment variables defined here
    def __del__(self):
        self.delMovieEnvVars()


    def debug(self, arg):
        mlogger.debug( arg )


    def info(self, arg):
        mlogger.info( arg )


    def warn(self, arg):
        mlogger.warning( arg )


    def error(self, errText, errCode=None):
        mlogger.error( errText.encode('utf-8') )
        if not errCode:
            sys.exit(1)
        else:
            sys.exit(errCode)
    
    
    def makeMovieDir(self):
        # Create movie directory under "Library"
        # Here we keep icon and background picture
        if not os.path.exists( self.movieDirPath ):
            try:
                os.mkdir( self.movieDirPath, 0750 )
                self.debug( "Movie data will be in '%s'" % self.movieDirPath )
            except OSError, errorText:
                self.error( "Can't create directory '%s': %s" % (self.movieDirPath, errorText) )
    ### end makeMovieDir ###
    
    
    def makeIconAsCategory(self):
        iconDest = os.path.join( self.movieDirPath, pydisconf.PYD_ICON_FILE )
        if os.path.exists( iconDest ):
            return
        os.environ[ 'PYD_CATEGORY_NAME' ] = self.movie.title
        os.environ[ 'PYD_CATEGORY_DIRPATH' ] = self.movieDirPath
        tmpIconCatWidth = os.environ[ 'PYD_ICON_CATEGORY_WIDTH' ]
        tmpIconCatHeight = os.environ[ 'PYD_ICON_CATEGORY_HEIGHT' ]
        os.environ[ 'PYD_ICON_CATEGORY_WIDTH' ] = str(pydisconf.PYD_ICON_WIDTH)
        os.environ[ 'PYD_ICON_CATEGORY_HEIGHT' ] = str(pydisconf.PYD_ICON_HEIGHT)
        os.system( pydisconf.PYD_SCR_MAKE_CAT_ICON )
        os.environ[ 'PYD_ICON_CATEGORY_WIDTH' ] = tmpIconCatWidth
        os.environ[ 'PYD_ICON_CATEGORY_HEIGHT' ] = tmpIconCatHeight
        self.warn( "Made icon for '%s' as category" % self.movie.title )
    ### makeIconAsCategory ###
    

    def makeIcon(self):
        
        if self.movie.isTV:
            numParts = len(self.movie.parts)
            if numParts < 2:
                self.makeIconAsCategory()
                return
        elif self.movie.isSet and not self.movie.set:
            self.makeIconAsCategory()
            return

        iconDest = os.path.join( self.movieDirPath, pydisconf.PYD_ICON_FILE )
        if not os.path.exists( iconDest ):
            iconSrc = os.path.join( pydisconf.PYD_YAMJ_DIR, self.movie.posterFile )
            if not os.path.exists( iconSrc ):
                self.warn( "Icon '%s' does not exist, make own" % iconSrc )
                self.makeIconAsCategory()
            else:
                os.environ[ 'PYD_SRC_ICON_IMAGE' ] = iconSrc
                os.environ[ 'PYD_DST_ICON_IMAGE' ] = iconDest
                os.system( pydisconf.PYD_SCR_MAKE_MOVIE_ICON )
                # Check once again if script made anything
                if not os.path.exists( iconDest ):
                    self.error( "Movie icon script did not produce an icon (%s)" % iconDest )
                else:
                    self.debug( "Icon '%s' was made by script '%s'" % ( iconDest, pydisconf.PYD_SCR_MAKE_MOVIE_ICON ) )
    ### end makeIcon ###
    
    
    def makeThumbnail(self):
        thumbDest = os.path.join( self.movieDirPath, pydisconf.PYD_ICON_THUMB_FILE )
        if not os.path.exists( thumbDest ):
            thumbSrc = os.path.join( pydisconf.PYD_YAMJ_DIR, self.movie.thumbnail )
            if not os.path.exists( thumbSrc ):
                self.error( "Thumbnail '%s' does not exist" % thumbSrc )
            # Check source and destination extension - if different, call script
            dotIndex = thumbDest.rindex( '.' )
            thumbDestExt = thumbDest[ dotIndex : ]
            dotIndex = thumbSrc.rindex( '.' )
            thumbSrcExt = thumbSrc[ dotIndex : ]
            if thumbDestExt != thumbSrcExt:
                os.environ[ 'PYD_SRC_THUMB_IMAGE' ] = thumbSrc
                os.environ[ 'PYD_DST_THUMB_IMAGE' ] = thumbDest
                os.system( pydisconf.PYD_SCR_MAKE_THUMB_IMAGE )
                self.debug( "Picture '%s' was converted into thumbnail '%s' by script '%s'" %
                    (thumbSrc, thumbDest, pydisconf.PYD_SCR_MAKE_THUMB_IMAGE) )
                # Check once again if script made anything
                if not os.path.exists( thumbDest ):
                    self.error( "Thumbnail script did not produce a thumbnail" )
            else:
                shutil.copyfile( thumbSrc, thumbDest )
                self.debug( "Thumbnail '%s' copied to '%s'" % ( thumbSrc, thumbDest ) )
    ### end makeThumbnail ###


    def makeBackgroundImage(self):
        bgrDest = os.path.join( self.movieDirPath, 'background.jpg' )
        # Make ugly hack to set background for movie set or TV series
        if self.movie.isSet:
            sourceBackground = self.movie.baseFilename + ".background.jpg"
        else:
            # Normal movie
            sourceBackground = self.movie.fanartFile

        if not os.path.exists( bgrDest ):
            if not sourceBackground:
                # Use default background image
                self.warn( "Background image for '%s' does not exist, using default" % \
                    ( self.movie.title ) )
                bgrSrc = pydisconf.PYD_BCKGR_IMAGE
            else:
                bgrSrc = os.path.join( pydisconf.PYD_YAMJ_DIR, sourceBackground )
            if not os.path.exists( bgrSrc ):
                self.error( "Source background '%s' does not exist" % bgrSrc )
            if self.movie.isSet:
                shutil.copyfile( bgrSrc, bgrDest )
                self.debug( "Background '%s' copied to '%s'" % ( bgrSrc, bgrDest ) )
            else:
                os.environ[ 'PYD_SRC_BCKGR_IMAGE' ] = bgrSrc
                os.environ[ 'PYD_DST_BCKGR_IMAGE' ] = bgrDest
                if self.movie.isTV:
                    os.environ[ 'PYD_MOV_IS_TVSET' ] = '1'
                os.system( pydisconf.PYD_SCR_MAKE_BCKGR_IMAGE )
                self.debug( "Picture '%s' was made a background '%s' by script '%s'" %
                    (bgrSrc, bgrDest, pydisconf.PYD_SCR_MAKE_BCKGR_IMAGE) )
    ### end makeBackgroundImage ###
    
    
    def copyDuneFolderTxt(self):
        duneFolderMovieFile = os.path.join( self.movieDirPath, 'dune_folder.txt' )
        self.duneFolderFile = duneFolderMovieFile
        # Determine which dune_folder template file to copy
        if self.movie.isSet:
            templateFile = pydisconf.PYD_MOVIESET_DUFO_TPL
        else:
            if self.movie.isTV:
                templateFile = pydisconf.PYD_TVSET_DUFO_TPL
            else:
                templateFile = pydisconf.PYD_MOVIE_DUFO_TPL
        retVal = os.path.exists( duneFolderMovieFile )
        if not retVal:
            PydUtil.copyTemplateFile( templateFile, duneFolderMovieFile )
        return retVal
    ### end copyDuneFolderTxt ###

    
    # Appends item that is part of movie set to "dune_folder.txt"
    def appendMovieSetItem(self, aMovie):
        if not aMovie:
            return
        if aMovie.originalTitle != aMovie.title:
            titleStr = "%s (%s)" % (aMovie.title, aMovie.originalTitle)
        else:
            titleStr = aMovie.title
        self.itemList.append( 'item.%d.caption = P%02d - %s\n' % ( self.dfIndex, self.dfIndex+1, titleStr ) )
        self.itemList.append( 'item.%d.media_action = browse\n' % ( self.dfIndex ) )
        self.itemList.append( 'item.%d.media_url = ../../Library/%s\n' % ( self.dfIndex, aMovie.baseFilename ) )
        self.itemList.append( 'item.%d.icon_path = ../../Library/%s/%s\n' % \
            ( self.dfIndex, aMovie.baseFilename, pydisconf.PYD_ICON_FILE ) )
        self.itemList.append( 'item.%d.icon_scale_factor = %s\n' % ( self.dfIndex, pydisconf.PYD_ICON_SCALE_FACTOR ) )
        if pydisconf.PYD_ICON_USE_SEL:
            self.itemList.append( 'item.%d.icon_sel_scale_factor = 1\n' % ( self.dfIndex ) )
        self.itemList.append( 'item.%d.icon_valign = center\n' % ( self.dfIndex ) )
        self.dfIndex = self.dfIndex + 1
    ### appendMovieSetItem ###


    def make1MoviePartItem(self, aPart):
        self.makeMovieDir()
        self.makeBackgroundImage()
        self.movie.isTV = False # To pull movie dune_folder.txt template
        self.copyDuneFolderTxt()
        self.movie.isTV = True
        # Temporary keep items we've gathered so far
        tempList = self.itemList
        self.itemList = []
        self.itemList.append( "paint_icon_selection_box = no\n" )
        self.itemList.append( "paint_icons = no\n" )
        if self.movie.originalTitle != self.movie.title:
            titleStr = "- (%s: %s)" % (self.movie.title, aPart.fileTitle)
        else:
            titleStr = self.movie.title
        self.itemList.append( "item.0.caption = %s E%02d %s\n" % \
            (self.movie.originalTitle, aPart.part, titleStr) )
        self.itemList.append( "item.0.media_url = %s\n" % aPart.fileURL )
        self.itemList.append( 'item.0.media_action = play\n' )
        self.saveDuneFolder()
        self.itemList = tempList
    ### make1MoviePartItem  ###
    
    
    # Creates everything necessery for movie part
    # (entries in dune_folder.txt, and a separate directories for TV episodes
    # under "seasonal" directory)
    def makeMoviePartItem(self, aPart):
        iconFileName = pydisconf.PYD_ICON_MASK % "_part%02d" % aPart.part
        tempMovieDirPath = self.movieDirPath
        episodeDir = "E%02d" % aPart.part
        
        if os.environ.has_key( 'PYD_PART_SEL_THUMB' ):
            del os.environ[ 'PYD_PART_SEL_THUMB' ]
            
        if self.movie.isTV:
            self.movieDirPath = os.path.join( self.movieDirPath, episodeDir )
            thumbPartDest = os.path.join( self.movieDirPath, pydisconf.PYD_ICON_FILE )
            self.make1MoviePartItem( aPart )
            if pydisconf.PYD_ICON_USE_SEL:
                thumbPartSelDest = os.path.join( self.movieDirPath, pydisconf.PYD_ICON_SEL_FILE )
                os.environ[ 'PYD_PART_SEL_THUMB' ] = thumbPartSelDest
        else:
            self.itemList.append( 'item.%d.caption = %s %d\n' % \
                ( self.dfIndex, self.movie.originalTitle, aPart.part ) )
            self.itemList.append( 'item.%d.icon_path = %s\n' % ( self.dfIndex, iconFileName ) )
            self.itemList.append( 'item.%d.media_action = play\n' % ( self.dfIndex ) )
            self.itemList.append( 'item.%d.media_url = %s\n' % ( self.dfIndex, aPart.fileURL ) )
            self.itemList.append( 'item.%d.icon_scale_factor = %s\n' % ( self.dfIndex, pydisconf.PYD_TVICON_SCALE_FACTOR ) )
            self.itemList.append( 'item.%d.icon_sel_scale_factor = 1\n' % ( self.dfIndex ) )
            self.itemList.append( 'item.%d.icon_valign = center\n' % ( self.dfIndex ) )
            thumbPartDest = os.path.join( self.movieDirPath, iconFileName )
        
        if os.path.exists( thumbPartDest ):
            self.movieDirPath = tempMovieDirPath
            return
        else:    
            os.environ[ 'PYD_PART_THUMB' ] = thumbPartDest
            os.environ[ 'PYD_PART_MOV' ] = str(aPart.part)
        
        if self.movie.isTV:
            # Add title, plot and videoimage
            os.environ[ 'PYD_PART_TITLE'  ] = aPart.fileTitle
            os.environ[ 'PYD_PART_PLOT'   ] = aPart.filePlot
            os.environ[ 'PYD_PART_AIRED'  ] = aPart.firstAired
            os.environ[ 'PYD_PART_VIDIMG' ] = os.path.join( pydisconf.PYD_YAMJ_DIR, aPart.fileImageFile )
    
        os.system( pydisconf.PYD_SCR_MAKE_PART_THUMB )
        self.debug( "Thumbnail '%s' for TV episode / movie part %d was made by script '%s'" % \
            (thumbPartDest, aPart.part, pydisconf.PYD_SCR_MAKE_PART_THUMB) )
          
        # Check if script produced anything
        if not os.path.exists( thumbPartDest ):
            self.error( "Thumbnail for '%s' (TV episode / part) %d does not exist" % \
                (self.movie.originalTitle, aPart.part) )

        self.dfIndex = self.dfIndex + 1
        self.movieDirPath = tempMovieDirPath
    ### makeMoviePartItem ###
    
    
    # Appends item that makes a movie
    def appendMovieParts(self):
        if len(self.movie.parts) == 0 and not self.movie.isSet:
            # Seems movie does not have information about actual file
            self.error( "Looks like movie does not have any part, aborting" )
        else:
            if len(self.movie.parts) == 1:
                # Normal movie - just append items to existing dune_folder.txt
                self.itemList.append( 'paint_icon_selection_box = no\n' )
                self.itemList.append( 'paint_icons = no\n' )
                self.itemList.append( 'icon_scale_factor = %s\n' % ( pydisconf.PYD_ICON_SCALE_FACTOR ) )
                self.itemList.append( 'icon_sel_scale_factor = 1\n' )
                if self.movie.originalTitle != self.movie.title:
                    titleStr = "%s (%s)" % (self.movie.title, self.movie.originalTitle)
                else:
                    titleStr = self.movie.title
                self.itemList.append( 'item.0.caption = %s\n' % ( titleStr ) )
                self.itemList.append( 'item.0.media_url = %s\n' % ( self.movie.parts[0].fileURL ) )
                self.itemList.append( 'item.0.media_action = play\n' )
            else:
                # Movie is in two or more parts (e.g. LOTR, Extended Edition) - or it is TV series
                # Create icons for each part. Movie starts when user presses corresponding one
                self.dfIndex = 0
                self.itemList.append( 'paint_icon_selection_box = yes\n' )
                self.itemList.append( 'paint_icons = yes\n' )
                
                for part in self.movie.parts:
                    self.makeMoviePartItem( part )
                ### for
                self.duneFolderFile = None
            self.saveDuneFolder()
    ### appendMovieParts ###


    # Append to dune_folder.txt everything that is in buffer
    def saveDuneFolder(self):
        if not self.duneFolderFile:
            self.duneFolderFile = os.path.join( self.movieDirPath, 'dune_folder.txt' )
        if len( self.itemList ) != 0:
            out = open( self.duneFolderFile, 'a' )
            out.writelines( self.itemList )
            out.close()
            self.debug( "Appended %d Dune items to %s" % ( len(self.itemList), self.duneFolderFile ) )
            self.itemList = []
    ### saveDuneFolder ###


    # Set environment variables based on movie data (title etc)
    # so that they are available in script that makes background image
    def setMovieEnvVars(self):
        os.environ[ 'PYD_MOV_TITLE' ] = self.movie.title
        os.environ[ 'PYD_MOV_ORIG_TITLE' ] = self.movie.originalTitle
        os.environ[ 'PYD_MOV_YEAR' ] = self.movie.year
        os.environ[ 'PYD_MOV_RELEASE_DATE' ] = self.movie.releaseDate
        os.environ[ 'PYD_MOV_PLOT' ] = self.movie.plot
        os.environ[ 'PYD_MOV_OUTLINE' ] = self.movie.outline
        os.environ[ 'PYD_MOV_QUOTE' ] = self.movie.quote
        os.environ[ 'PYD_MOV_TAGLINE' ] = self.movie.tagline
        os.environ[ 'PYD_MOV_COUNTRY' ] = self.movie.country
        os.environ[ 'PYD_MOV_COMPANY' ] = self.movie.company
        os.environ[ 'PYD_MOV_RUNTIME' ] = self.movie.runtime
        os.environ[ 'PYD_MOV_CERT' ] = self.movie.certification
        os.environ[ 'PYD_MOV_LANG' ] = self.movie.language
        os.environ[ 'PYD_MOV_SUBTITLES' ] = self.movie.subtitles
        os.environ[ 'PYD_MOV_VCODEC' ] = self.movie.videoCodec
        os.environ[ 'PYD_MOV_ACODEC' ] = self.movie.audioCodec
        os.environ[ 'PYD_MOV_ASPECT' ] = self.movie.aspect
        os.environ[ 'PYD_MOV_FPS' ] = self.movie.fps
        os.environ[ 'PYD_MOV_DIRECTORS' ] = ", ".join( self.movie.directors )
        os.environ[ 'PYD_MOV_WRITERS' ] = ", ".join( self.movie.writers )
        os.environ[ 'PYD_MOV_ACTORS' ] = ", ".join( self.movie.actors )
    ### setMovieEnvVars ###
    
    
    def delEnvVar(self, aEnv):
        if os.environ.has_key( aEnv ):
            del os.environ[ aEnv ]
 
 
    def delMovieEnvVars(self):
        eVars = ( 'PYD_SRC_BCKGR_IMAGE', 'PYD_DST_BCKGR_IMAGE', 'PYD_SRC_THUMB_IMAGE', 'PYD_DST_THUMB_IMAGE', \
            'PYD_MOV_TITLE', 'PYD_MOV_ORIG_TITLE', 'PYD_MOV_YEAR', 'PYD_MOV_RELEASE_DATE', 'PYD_MOV_PLOT', \
            'PYD_MOV_OUTLINE', 'PYD_MOV_QUOTE', 'PYD_MOV_TAGLINE', 'PYD_MOV_COUNTRY', 'PYD_MOV_COMPANY', \
            'PYD_MOV_RUNTIME', 'PYD_MOV_CERT', 'PYD_MOV_LANG', 'PYD_MOV_SUBTITLES', 'PYD_MOV_VCODEC', \
            'PYD_MOV_ACODEC', 'PYD_MOV_ASPECT', 'PYD_MOV_FPS', 'PYD_MOV_DIRECTORS', 'PYD_MOV_RATINGS', \
            'PYD_MOV_WRITERS', 'PYD_MOV_ACTORS', 'PYD_MOV_IS_TVSET', 'PYD_PART_THUMB', 'PYD_PART_SEL_THUMB' \
            'PYD_PART_MOV' )
        map( self.delEnvVar, eVars )
    ### delMovieEnvVars ###


    # Generate all objects for a movie (icon etc.)
    def make(self, aSkipParse=False):
        
        # Check if movie is initialised
        if not self.movie:
            self.error( "Movie element was not initialised" )
        self.movieYAMJPath = os.path.join( pydisconf.PYD_YAMJ_DIR, self.movie.baseFilename + ".xml" )
        self.movieDirPath = os.path.join( pydisconf.PYD_OUT_DIR, 'Library', self.movie.baseFilename )
        
        self.makeMovieDir()
        if not aSkipParse:
            # Usually a movie set
            self.debug( "Parsing file %s" % self.movieYAMJPath )
            self.parser.parse( self.movieYAMJPath )
        else:
            self.mprs.movies.append( self.movie )
            
        for mov in self.mprs.movies:
            self.movie = mov
            self.debug( self.movie )
            self.setMovieEnvVars()
            self.makeThumbnail()
            self.makeIcon()
            self.makeBackgroundImage()
            if not self.copyDuneFolderTxt():
                self.appendMovieParts()
            self.delMovieEnvVars()
        ### for
    ### make ###

