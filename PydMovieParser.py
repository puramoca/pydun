# -*- coding: utf-8 -*-

import logging
import sys
import xml.sax
import urllib

import pydisconf
import PydMovie
import PydMoviePart


mlogger = logging.getLogger( 'PydMovieParser' )
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel( logging.INFO )
# Set a format which is simpler for console use
consoleFormatter = logging.Formatter( pydisconf.PYD_LOG_CONSOLE_FORMAT )
consoleHandler.setFormatter( consoleFormatter )
mlogger.addHandler( consoleHandler )


class PydMovieParser(xml.sax.handler.ContentHandler):
    
    def __init__(self):
        self.currData = None
        self.currElem = None
        self.logger = logging.getLogger( __name__ )
        self.movies = []
        self.movie = None
        # Regular movie elements that do not require any special handling
        self.movieElems = ( 'year', 'releaseDate', 'top250', 'plot', 'outline', 'quote', 'tagline', 'country', 'company', 'runtime', 'certification', 'language', 'subtitles', 'container', 'videoCodec', 'audioCodec', 'audioChannels', 'resolution', 'videoSource', 'videoOutput', 'aspect', 'fps', 'season', 'set' )
        # Movie elements that can contain characters like & or '
        self.movieXmlSensitive = ( 'title', 'originalTitle' )
        # Some attributes we like without special chars
        self.movieReplAttrs = ( 'baseFilenameBase', 'baseFilename' )
        # Some attributes we must urllib-unquote
        self.movieUnqAttrs = ( 'posterFile', 'detailPosterFile', 'fanartFile', 'thumbnail', 'bannerFile', 'clearlogoFile', 'clearartFile', 'tvthumbFile' )
        self.movieListAttrs = ( 'director', 'writer', 'actor' )
        self.movieHashAttrs = ( 'rating' )
        # Attributes appearing under <file>...</file> section
        self.moviePartsAttrs = ( 'filelocation', 'filetitle', 'firstaired', 'fileplot', 'fileimagefile', 'fileurl' )
        self.moviedb = None
        self.moviepart = None


    def debug(self, arg):
        mlogger.debug( str(arg).encode('utf-8') )


    def error(self, errText, errCode=None):
        mlogger.error( str(errText) )
        if not errCode:
            sys.exit(1)
        else:
            sys.exit(errCode)


    def startElement(self, aName, attrs):
        if aName.lower() == 'movie':
            self.movie = PydMovie.PydMovie()
            # Check if "movie" is actually a set or TV season
            if attrs.has_key( 'isSet' ):
                self.movie.isSet = attrs[ 'isSet' ].lower() == 'true'
            if attrs.has_key( 'isTV' ):
                self.movie.isTV = attrs[ 'isTV' ].lower() == 'true'
        elif aName.lower() in self.movieHashAttrs:
            if attrs.has_key( 'moviedb' ):
                self.moviedb = attrs[ 'moviedb' ]
                if aName == 'rating':
                    if not self.movie.ratings.has_key( self.moviedb ):
                        self.movie.ratings[ self.moviedb ] = None
        elif aName.lower() == 'file':
            self.moviepart = PydMoviePart.PydMoviePart()
        elif aName.lower() in self.moviePartsAttrs:
            if attrs.has_key( 'part' ) and not self.moviepart.part:
                self.moviepart.part = int( attrs[ 'part' ] )
        elif aName in self.movieXmlSensitive:
            setattr( self.movie, aName, '' )
        self.currElem = aName


    def endElement(self, aName):
        if not self.movie:
            return
        if aName.lower() == 'movie':
            self.movies.append( self.movie )
            self.movie = None
        elif aName.lower() == 'file':
            self.movie.parts.append( self.moviepart )
            self.moviepart = None
        elif aName in self.movieElems:
            setattr( self.movie, aName, self.currData )
        elif aName in self.movieReplAttrs :
            setattr( self.movie, aName, self.currData )
        elif aName in self.movieUnqAttrs:
            setattr( self.movie, aName, urllib.unquote(self.currData) )
        elif aName in self.movieXmlSensitive:
			setattr( self.movie, aName, getattr( self.movie, aName ).strip() )
        elif aName in self.movieListAttrs:
            if aName == 'director' and self.currData not in self.movie.directors:
                self.movie.directors.append( self.currData )
            elif aName == 'writer' and self.currData not in self.movie.writers:
                self.movie.writers.append( self.currData )
            elif aName == 'actor' and self.currData not in self.movie.actors:
                self.movie.actors.append( self.currData )
        elif aName in self.movieHashAttrs:
            if aName == 'rating':
                self.movie.ratings[ self.moviedb ] = self.currData
        elif aName.lower() in self.moviePartsAttrs:
            setattr( self.moviepart, aName, urllib.unquote( self.currData ) )


    def characters(self, data):
        if data in ( 'UNKNOWN' ):
            self.currData = ''
        else:
            self.currData = data.strip().encode('utf-8')
        # print "'" + self.currData + "'"
        if self.currElem in self.movieXmlSensitive and self.currData != '':
            setattr( self.movie, self.currElem, getattr(self.movie, self.currElem) + self.currData + " " )		
### end class PydMovieParser
