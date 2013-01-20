# Identification division

# Configuration section
import glob
import logging
import os
import shutil
import sys
import xml.sax

import pydisconf
import PydMovieParser
import PydUtil


mlogger = logging.getLogger( 'PydCategoryDir' )
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel( logging.INFO )
# Set a format which is simpler for console use
consoleFormatter = logging.Formatter( pydisconf.PYD_LOG_CONSOLE_FORMAT )
consoleHandler.setFormatter( consoleFormatter )
mlogger.addHandler( consoleHandler )


class PydCategoryDir:

    def __init__(self):
        self.parser = xml.sax.make_parser()
        self.movieParser = PydMovieParser.PydMovieParser()
        self.parser.setContentHandler( self.movieParser )


    def __del__(self):
        if os.environ.has_key( 'PYD_CATEGORY' ):
            del os.environ[ 'PYD_CATEGORY' ]
        if os.environ.has_key( 'PYD_CATEGORY_DIRPATH' ):
            del os.environ[ 'PYD_CATEGORY_DIRPATH' ]
        if os.environ.has_key( 'PYD_CATEGORY_NAME' ):
            del os.environ[ 'PYD_CATEGORY_NAME' ]
        if os.environ.has_key( 'PYD_CATEGORY' ):
            del os.environ[ 'PYD_CATEGORY' ]


    def debug(self, aText):
        mlogger.debug( str(aText).encode('utf-8') )


    def warn(self, aText):
        mlogger.warning( str(aText).encode('utf-8') )
        

    def error(self, errText, errCode=None):
        mlogger.error( str(errText) )
        if not errCode:
            sys.exit(1)
        else:
            sys.exit(errCode)


    def makeIcons(self, aDirPath):
        iconPath = os.path.join( aDirPath, pydisconf.PYD_ICON_CAT_FILE )
        if pydisconf.PYD_ICON_USE_SEL:
            iconSelPath = os.path.join( aDirPath, pydisconf.PYD_ICON_CAT_SEL_FILE )
        
        if pydisconf.PYD_CLEAN_OUT_DIR or not os.path.exists( iconPath ):
            # Make icon or copy existing one
            os.system( pydisconf.PYD_SCR_MAKE_CAT_ICON )
            self.debug( "Icon '%s' was made by script '%s'" % (iconPath, pydisconf.PYD_SCR_MAKE_CAT_ICON))

        # Check if script produced icon
        if not os.path.exists( iconPath ):
            self.error( "Icon '%s' does not exist" % iconPath )
        # If true, check existance of "selected" icon too
        if pydisconf.PYD_ICON_USE_SEL:    
            if not os.path.exists( iconSelPath ):
                self.error( "Selected icon %s does not exist" % iconSelPath )
    ### end makeIcons ###  


    def makeItemList(self, aPathCategoryMask):
        lItem = []
        if not aPathCategoryMask or aPathCategoryMask == '':
            return lItem
        lIndex = 0
        catList = sorted(glob.glob( aPathCategoryMask ))
        
        for catFile in catList:
            self.debug( "Parsing category file '%s'" % catFile  )
            self.parser.parse( catFile )
            
            for movie in self.movieParser.movies:
                lItem.append( 'item.%d.caption = %05d - %s\n' % ( lIndex, lIndex + 1, movie.originalTitle ) )
                lItem.append( 'item.%d.media_action = browse\n' % ( lIndex ) )
                lItem.append( 'item.%d.media_url = ../../Library/%s\n' % ( lIndex, movie.baseFilename ) )
                if movie.isSet:
                    lIconFile = pydisconf.PYD_ICON_CAT_FILE
                else:
                    lIconFile = pydisconf.PYD_ICON_FILE
                lItem.append( 'item.%d.icon_path = ../../Library/%s/%s\n' % \
                    ( lIndex, movie.baseFilename, lIconFile ) )
                lItem.append( 'item.%d.icon_sel_path = ../../Library/%s/%s\n' % \
                    ( lIndex, movie.baseFilename, lIconFile ) )
                lItem.append( 'item.%d.icon_scale_factor = %s\n' % ( lIndex, pydisconf.PYD_ICON_SCALE_FACTOR ) )
                lItem.append( 'item.%d.icon_sel_scale_factor = 1\n' % ( lIndex ) )
                lItem.append( 'item.%d.icon_valign = center\n' % ( lIndex ) )
                lIndex = lIndex + 1
            self.movieParser.movies = []
        return lItem
    ### makeItemList ###
    
    
    def makeSubCategories(self, aDirPath, aSubcategories):
        
        for (name, origName, fileMask) in aSubcategories:
            fileName = self.getNameFromMask( fileMask )
            os.environ[ 'PYD_CATEGORY' ] = fileName
            os.environ[ 'PYD_CATEGORY_NAME' ] = name.encode('utf-8')
            dirPath2 = self.makeDirPath( aDirPath, fileName )
            self.makeCategory( dirPath2 )
            
            os.environ[ 'PYD_CATEGORY_DIRPATH' ] = dirPath2
            # Make icon or copy existing one
            self.makeIcons( dirPath2 )
            
            # Make 'dune_folder.txt' for sub-category
            duneFolderCatFile = os.path.join( dirPath2, 'dune_folder.txt' )
            if not os.path.exists( duneFolderCatFile ):
                PydUtil.copyTemplateFile( pydisconf.PYD_SUBCAT_DUFO_TPL, duneFolderCatFile )
            
                # Read all files for each file mask
                pathCategoryMask = os.path.join( pydisconf.PYD_YAMJ_DIR, fileMask)
                # Create list of items for given 'dune_folder.txt'
                itemList = self.makeItemList( pathCategoryMask )
                # Append list of these items to 'dune_folder.txt'
                out = open( duneFolderCatFile, 'a' )
                out.writelines( itemList )
                out.close()
                itemNum = len(itemList) / 8
                self.debug( "Added %d movie items" % itemNum )
    ### makeSubCategories ###
    
    
    def makeTLCategories(self, aDict):
        if not aDict or aDict == {}:
            self.error( "Categories are not defined" )
            
        # Walk over top categories
        for (category, subcats) in aDict.items():
            if category == 'Library':
                dirPath = self.makeDirPath( pydisconf.PYD_OUT_DIR, category )
                self.makeCategory( dirPath )
                continue
            os.environ[ 'PYD_CATEGORY' ] = category
            os.environ[ 'PYD_CATEGORY_NAME' ] = category
            
            dirPath = self.makeDirPath( pydisconf.PYD_OUT_DIR, category)
            self.makeCategory( dirPath )
            os.environ[ 'PYD_CATEGORY_DIRPATH' ] = dirPath
            self.makeIcons( dirPath )
            
            duneFolderCatFile = os.path.join(dirPath, 'dune_folder.txt')
            if not os.path.exists( duneFolderCatFile ):
                PydUtil.copyTemplateFile( pydisconf.PYD_CAT_DUFO_TPL, duneFolderCatFile )
            
            # Walk over sub-categories
            self.makeSubCategories(dirPath, subcats)
    ### makeTLCategories ###
    
                  
    def makeCategory(self, aDirCat):
        if not os.path.exists( aDirCat ):
            try:
                os.mkdir( aDirCat, 0750 )
                self.debug( "Made directory '%s'" % aDirCat )
            except OSError:
                self.error( "Cannot create directory '%s'" % aDirCat )
    ### makeCategory ###
    
    
    def makeDirPath(self, aBaseDir=None, aDir=None):
        if not aBaseDir or not aDir:
            return
        lDir = aDir.replace( ' ', '_' )
        lDir = os.path.join( aBaseDir, lDir )
        return lDir
    ### makeDirPath ###
    
    
    def getNameFromMask(self, aName):
        leftUnderscore = aName.find( '_' )
        rightUnderscore = aName.rfind( '_' )
        if leftUnderscore > -1 and rightUnderscore > -1:
            return aName[ leftUnderscore + 1 : rightUnderscore ]
    ### getNameFromMask ###
    
### end class CategoryDir ###
