#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Identification division

# Configuration section
import getopt
import glob
import logging
import os
import shutil
import sys
import xml.sax

import PydCategory
import PydCategoryDir
import PydMovie
import PydMovieDir
import PydMovieParser
import PydUtil
import movielib
import pydisconf

G_LONG_OPTS = ["config=", "help", "debug="]
G_SHORT_OPTS = "c:hd:"
G_LOG_LEVEL = 20 # INFO
log = None


def printUsage():
    print
    print "Usage: %s [-c|--config] <configuration_file> [-d|--debug] level" % sys.argv[0]
    sys.exit(2)
### end printUsage ###

    
def error(errText, errCode=None):
    global log
    log.error( str(errText) )
    if not errCode:
        sys.exit(1)
    else:
        sys.exit(errCode)


def parseArgs(opts):
    global G_LOG_LEVEL, log
    
    for o, a in opts:
        if o in ( "-d", "--debug" ):
            G_LOG_LEVEL = getattr( logging, a.upper(), None )
         
        if o in ( "-c", "--config" ):
            pydisconf.PYD_CONFIG_FILE = os.path.abspath( os.path.normpath(a) )

    if not isinstance(G_LOG_LEVEL, int):
        raise ValueError( 'Invalid log level: %s' % G_LOG_LEVEL)
### end parseArgs ###


# Removes all files and subdirectories under "aDir"
def removeAll( aDir ):
    global log
    log.info( "Removing files and directories under " + aDir )
    
    if os.path.abspath( aDir ) == '/':
        return
    for root, dirs, files in os.walk( aDir, topdown=False ):
        for name in files:
            fname = os.path.join(root, name)
            os.remove( fname )
        for name in dirs:
            dname = os.path.join(root, name)
            os.rmdir( dname )
### end makeCategoryDirs ###


# Copies top-level items to appropriate directories
def copyTopLevelItems():
    global log
    # Copy top-level dune_folder template
    src = os.path.join( pydisconf.PYD_TPL_DIR, pydisconf.PYD_TL_DUFO_TPL )
    if not os.path.exists( src ):
        error( "Top-level dune_folder.txt template '%s' does not exist" % src )
        
    dst = os.path.join( pydisconf.PYD_OUT_DIR, 'dune_folder.txt' )
    PydUtil.copyTemplateFile( src, dst )
    
    # Copy background image to top-level directory
    dst = os.path.join( pydisconf.PYD_OUT_DIR, 'background.jpg' )
    shutil.copyfile( pydisconf.PYD_BCKGR_IMAGE, dst )
    log.debug( "Copied background image '%s' to '%s'" % (src, dst) )
    
    # Copy icon
    if not os.path.exists( pydisconf.PYD_LOGO_IMAGE ):
        error( "Logo image '%s' does not exist" % pydisconf.PYD_LOGO_IMAGE )
    dst = os.path.join( pydisconf.PYD_OUT_DIR, pydisconf.PYD_ICON_FILE )
    shutil.copyfile( pydisconf.PYD_LOGO_IMAGE, dst )
### end copyTopLevelItems ###


# Function that returns list of episodes or movie parts
# found in XML file "aFilename"
def getParts( aFilename ):
    libParts = movielib.MovieLib()
    partsPath = os.path.join( pydisconf.PYD_YAMJ_DIR, aFilename )
    libParts.parse( partsPath )
    partsList = libParts.getMovies()
    return partsList
### end getParts ###


def makeSetElements( aMovie ):
    if not aMovie.isSet:
        return
    movieD = PydMovieDir.PydMovieDir()
    movieD.movie = aMovie
    movieD.make(True)
    return movieD
### makeSetElements ###


# Function that makes all elements in movie directory
# (background, thumbnail etc)
def makeMovieElements( aMovie ):
    movieD = PydMovieDir.PydMovieDir()
    movieD.movie = aMovie
    movieD.make()
### end makeMovieElements ###


if __name__ == "__main__":
    
    # Check number of arguments passed
    if len(sys.argv) == 1:
        printUsage()
    
    try:
        opts, args = getopt.getopt( sys.argv[1:], G_SHORT_OPTS, G_LONG_OPTS )
    except getopt.GetoptError, errorText:
        printUsage()
        error( str(errorText) )
			
    parseArgs(opts)

    # Initialise configuration
    pydisconf.init()

    logging.basicConfig(level=G_LOG_LEVEL,
        format=pydisconf.PYD_LOG_FILE_FORMAT,
        datefmt='%m-%d %H:%M',
        filename=pydisconf.PYD_LOG_FILE,
        filemode='a')

    log = logging.getLogger( __name__ )
    
    log.debug( " " )
    log.debug( "Logging started" )
    log.debug( " " )
    
    # Debug configuration to file
    pydisconf.debug()
    
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel( logging.INFO )
    # Set a format which is simpler for console use
    consoleFormatter = logging.Formatter( pydisconf.PYD_LOG_CONSOLE_FORMAT )
    consoleHandler.setFormatter( consoleFormatter )

    # add the handler to the root logger
    log.addHandler( consoleHandler )
    
    log.debug( "Configuration file: " + pydisconf.PYD_CONFIG_FILE )
    
    try:
        os.mkdir( pydisconf.PYD_OUT_DIR, 0750 )
        log.debug( "Created directory %s" % pydisconf.PYD_OUT_DIR )
    except OSError:
        pass
        
    # Create top-level directory and optionally make it empty
    if pydisconf.PYD_CLEAN_OUT_DIR:
        removeAll( pydisconf.PYD_OUT_DIR )
        # Copy top-level items
    copyTopLevelItems()
            
    # Start parsing categories
    catparse = PydCategory.PydCategory()
    catparse.parse( os.path.join( pydisconf.PYD_YAMJ_DIR, "Categories.xml" ) )
    
    # Create top level categories and their sub-categories
    catdir = PydCategoryDir.PydCategoryDir()
    categories = catparse.getCategories()
    catdir.makeTLCategories( categories )

    # Get everything from "Library" category
    catLibrary = categories[ "Library" ]
    
    for library in catLibrary:
        log.info( "Processing library file(s): %s" % library[2] )
        libPattern = os.path.join( pydisconf.PYD_YAMJ_DIR, library[2] )
        
        libList = sorted(glob.glob( libPattern ))
        
        for libFile in libList:  

            libmov = movielib.MovieLib()
            
            if not os.path.exists( libFile ):
                log.warning( "Library file '%s' does not exist, skipping ..." % libFile )
                continue

            libmov.parse( libFile )
            movies = libmov.getMovies()

            for movie in movies:

                if movie.isSet:
                    
                    movieDir = makeSetElements( movie )
                    if movie.isTV:
                        # We have TV series; create directory and sub-directories
                        # corresponding to each season
                        seasons = getParts( movie.baseFilename + ".xml" )
                        
                        for season in seasons:
                            # Parse each season
                            makeMovieElements( season )
                            movieDir.appendMovieSetItem( season )
                        # for season ...
                    else:
                        # Just a movie set; create just one subdirectory for
                        # displaying icons for each movie
                        episodes = getParts( movie.baseFilename + ".xml" )
                        
                        for episode in episodes:
                            epMovie = getParts( episode.baseFilename + ".xml" )[0]
                            makeMovieElements( epMovie )
                            movieDir.appendMovieSetItem( epMovie )
                    # if movie.isTV
                    movieDir.saveDuneFolder()
                else:
                    try:
                        makeMovieElements( movie )
                    except:
                        print "Movie exception in",movie.title 
                # if movie.isSet
            # for movie ...
            libmov = None
        ### for libFile in libList
    ### for library in catLibrary
    
    log.debug( " " )
    log.debug( "Logging ended" )
