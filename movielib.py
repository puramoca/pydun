# Identification division

# Configuration section
import logging
import os
import sys
import xml.sax

import PydMovieParser


class MovieLib:
    
    def __init__(self):
        self.parser = xml.sax.make_parser()
        self.parserClass = PydMovieParser.PydMovieParser()
        self.parser.setContentHandler( self.parserClass )
        self.logger = logging.getLogger( __name__ )
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel( logging.INFO )
        # Set a format which is simpler for console use
        consoleFormatter = logging.Formatter( '%(name)-14s: %(levelname)-8s %(message)s' )
        consoleHandler.setFormatter( consoleFormatter )
        self.logger.addHandler( consoleHandler )
        
    def debug(self, arg):
        self.logger.debug( str(arg).encode('utf-8') )


    def info(self, arg):
        self.logger.info( str(arg).encode('utf-8') )


    def error(self, errText, errCode=None):
        self.logger.error( str(errText).encode('utf-8') )
        if not errCode:
            sys.exit(1)
        else:
            sys.exit(errCode)


    def parse(self, aFile):
        if not os.path.exists( aFile ):
            self.error( "File '%s' does not exist" % aFile )
        self.parser.parse( aFile )

            
    def getMovies(self):
        return self.parserClass.movies
