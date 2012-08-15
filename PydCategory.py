
# Configuration section
import logging
import os
import sys
import xml.sax

import pydisconf
import PydCategoryParser


mlogger = logging.getLogger( 'PydCategory' )
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel( logging.INFO )
# Set a format which is simpler for console use
consoleFormatter = logging.Formatter( pydisconf.PYD_LOG_CONSOLE_FORMAT )
consoleHandler.setFormatter( consoleFormatter )
mlogger.addHandler( consoleHandler )


class PydCategory:
    
    def __init__(self):
        self.parser = xml.sax.make_parser()
        self.parserClass = PydCategoryParser.PydCategoryParser()
        self.parser.setContentHandler( self.parserClass )
        
    
    def error(self, errText, errCode=None):
        mlogger.error( str(errText).encode('utf-8') )
        if not errCode:
            sys.exit(1)
        else:
            sys.exit(errCode)
    
    def debug(self, arg):
        mlogger.debug( str(arg).encode('utf-8') )


    def parse(self, aFile):
        if not os.path.exists( aFile ):
            self.error( "File '%s' does not exist" % aFile )
        self.debug( "Parsing file '%s'" % aFile )
        self.parser.parse( aFile )
        self.debug( "Dictionary = %s" % self.parserClass.categories )
            
    def getCategories(self):
        return self.parserClass.categories
    
### PydCategory ###
