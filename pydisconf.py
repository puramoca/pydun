
# Configuration section
import logging
import os
import sys
import ConfigParser


PYD_CONFIG_FILE          = None
PYD_LOG_FILE             = None
PYD_OUT_DIR              = None
PYD_CLEAN_OUT_DIR        = None
PYD_TL_DUFO_TPL          = None
PYD_CAT_DUFO_TPL         = None
PYD_SUBCAT_DUFO_TPL      = None
PYD_MOVIE_DUFO_TPL       = None
PYD_MOVIESET_DUFO_TPL    = None
PYD_TVSET_DUFO_TPL       = None
PYD_TPL_DIR              = None
PYD_IMAGE_DIR            = None
PYD_LOGO_IMAGE           = None
PYD_BCKGR_IMAGE          = None
PYD_ICON_CAT_FILE        = None
PYD_ICON_CAT_SEL_FILE    = None
PYD_ICON_FILE            = None
PYD_ICON_THUMB_FILE      = None
PYD_ICON_SEL_FILE        = None
PYD_ICON_USE_SEL         = None # "True" if "selected" icon should be used
PYD_ICON_WIDTH           = 315
PYD_ICON_HEIGHT          = 455
PYD_ICON_CATEGORY_WIDTH  = 377
PYD_ICON_CATEGORY_HEIGHT = 233
PYD_ICON_SCALE_FACTOR    = 0.85
PYD_ICON_DEFAULT         = None # File name of default movie/category icon
PYD_ICON_MASK            = 'icon%%s.jpg' # Mask to create other icons
PYD_ICON_CAT_MASK        = 'icon%%s.jpg'
PYD_LANG                 = 'en'
PYD_LOCALE_DIR           = None
PYD_TVICON_SCALE_FACTOR  = 1
PYD_YAMJ_DIR             = None # Directory with items produced by YAMJ
PYD_SCRIPTS_DIR          = None
PYD_THEME                = 'default'
PYD_THEME_DIR            = None
PYD_SCR_MAKE_CAT_ICON    = None
PYD_SCR_MAKE_BCKGR_IMAGE = None
PYD_SCR_MAKE_THUMB_IMAGE = None # Script that makes thumbnail image
PYD_SCR_MAKE_PART_THUMB  = None # Script that makes thumbnail to start movie part
PYD_SCR_MAKE_EP_THUMB    = None
MYSELF                   = 'PYDIS'
IMAGE_SECTION            = 'IMAGE'
TEMPLATE_SECTION         = 'TEMPLATE'
SCRIPT_SECTION           = 'SCRIPT'
THEME_SECTION            = 'THEME'
PYD_LOG_CONSOLE_FORMAT   = '%(name)-12s: %(levelname)-8s %(message)s' # Mask for writing logging messages
PYD_LOG_FILE_FORMAT      = '%(asctime)s %(name)-14s %(levelname)-8s %(message)s'



CONFIG_DEFAULTS = {
        'TL.Dune.Folder.Templ'          : 'dune_folder_toplevel_template.txt',
        'category.dune.folder.templ'    : 'dune_folder_category_template.txt',
        'subcategory.dune.folder.templ' : 'dune_folder_subcategory_template.txt',
        'movie.dune.folder.templ'       : 'dune_folder_movie_template.txt',
        'movieset.dune.folder.templ'    : 'dune_folder_movieset_template.txt',
        'tvset.dune.folder.templ'       : 'dune_folder_tvset_template.txt',
        'default.background.image'      : 'background.jpg',
        'logo.image'                    : 'logo.jpg',
        'icon.mask'                     : 'icon%%s.jpg',
        'icon.use.selected'             : 1,
        'icon.width'                    : PYD_ICON_WIDTH,
        'icon.height'                   : PYD_ICON_HEIGHT,
        'icon.category.width'           : PYD_ICON_CATEGORY_WIDTH,
        'icon.category.height'          : PYD_ICON_CATEGORY_HEIGHT,
        'icon.scale.factor'             : PYD_ICON_SCALE_FACTOR,
        'icon.tvepisode.scale.factor'   : PYD_TVICON_SCALE_FACTOR,
        'theme.dir'                     : './theme/',
        'theme'                         : 'default'
}

if os.name == 'nt':
    _CONFIG_WINDOWS = {
        'output.directory'              : "C:\Temp\%s" % MYSELF,
        'log.file'                      : 'C:\Temp\%s.log' % MYSELF,
        'script.make.category.icon'     : 'makeCategoryIcon.cmd',
        'script.make.background.image'  : 'makeBackgroundImage.cmd',
        'script.make.thumbnail.image'   : 'makeThumbnailImage.cmd',
        'script.make.part.thumbnail'    : 'makePartThumbnail.cmd',
        'script.make.episode.thumbnail' : 'makeEpisodeThumbnail.cmd',
        'script.make.movie.icon'        : 'makeMovieIcon.cmd'
    }
    for (name, value) in _CONFIG_WINDOWS.items():
        CONFIG_DEFAULTS[ name ] = value
else:
    _CONFIG_UNIX = {
        'output.directory'              : '/tmp/%s' % MYSELF,
        'log.file'                      : '/tmp/%s.log' % MYSELF,
        'script.make.category.icon'     : 'makeCategoryIcon.sh',
        'script.make.background.image'  : 'makeBackgroundImage.sh',
        'script.make.thumbnail.image'   : 'makeThumbnailImage.sh',
        'script.make.part.thumbnail'    : 'makePartThumbnail.sh',
        'script.make.episode.thumbnail' : 'makeEpisodeThumbnail.sh',
        'script.make.movie.icon'        : 'makeMovieIcon.sh'
    }
    for (name, value) in _CONFIG_UNIX.items():
        CONFIG_DEFAULTS[ name ] = value

log = logging.getLogger( MYSELF + "Conf" )


def error(errText, errCode=None):
    log.error( str(errText) )
    if not errCode:
        sys.exit(1)
    else:
        sys.exit(errCode)

def debugText( logText ):
    log.debug( logText )


def checkConfig( config ):
    global log
    global MYSELF, PYD_LOG_FILE, PYD_OUT_DIR, PYD_YAMJ_DIR, PYD_CLEAN_OUT_DIR, PYD_ICON_FILE
    global PYD_TL_DUFO_TPL, PYD_CAT_DUFO_TPL, PYD_TPL_DIR, PYD_IMAGE_DIR, PYD_BCKGR_IMAGE
    global PYD_SCRIPTS_DIR, PYD_SCR_MAKE_CAT_ICON, PYD_ICON_SEL_FILE, IMAGE_SECTION
    global PYD_ICON_USE_SEL, PYD_ICON_WIDTH, PYD_ICON_HEIGHT, PYD_SUBCAT_DUFO_TPL
    global PYD_ICON_SCALE_FACTOR, PYD_MOVIE_DUFO_TPL, PYD_SCR_MAKE_BCKGR_IMAGE
    global PYD_MOVIESET_DUFO_TPL, PYD_TVSET_DUFO_TPL, PYD_ICON_THUMB_FILE
    global PYD_SCR_MAKE_THUMB_IMAGE, PYD_SCR_MAKE_PART_THUMB, PYD_SCR_MAKE_EP_THUMB
    global PYD_TVICON_SCALE_FACTOR, PYD_ICON_MASK, PYD_THEME_DIR, PYD_LOGO_IMAGE
    global PYD_SCR_MAKE_MOVIE_ICON, PYD_ICON_DEFAULT, PYD_ICON_CATEGORY_WIDTH
    global PYD_ICON_CATEGORY_HEIGHT, PYD_ICON_CAT_MASK, PYD_ICON_CAT_FILE
    global PYD_ICON_CAT_SEL_FILE, PYD_LANG, PYD_LOCALE_DIR
    
    if not config.has_section( 'YAMJ' ):
        error( "Configuration file does not have section 'YAMJ'" )
    if not config.has_section( MYSELF ):
        error( "Configuration file does not have section '%s'" % MYSELF )
    
    PYD_LOG_FILE = config.get( MYSELF, 'log.file' )
    os.environ[ 'PYD_LOG_FILE' ] = PYD_LOG_FILE
    
    # Log errors to console as well
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel( logging.ERROR )
    # Set a format which is simpler for console use
    consoleFormatter = logging.Formatter( PYD_LOG_CONSOLE_FORMAT )
    consoleHandler.setFormatter( consoleFormatter )
    log.addHandler( consoleHandler )
    
    imageSectionName = "%s-%s" % (MYSELF, IMAGE_SECTION)
    templateSectionName = "%s-%s" % (MYSELF, TEMPLATE_SECTION)
    scriptSectionName = "%s-%s" % (MYSELF, SCRIPT_SECTION)
    themeSectionName = "%s-%s" % (MYSELF, THEME_SECTION)
    
    PYD_OUT_DIR = config.get( MYSELF, 'output.directory' )
    os.environ[ 'PYD_OUT_DIR' ] = PYD_OUT_DIR
    
    PYD_YAMJ_DIR = config.get( 'YAMJ', 'Directory' )
    PYD_YAMJ_DIR = os.path.abspath( os.path.normpath(PYD_YAMJ_DIR) )
    if not os.path.exists( PYD_YAMJ_DIR ):
        error( "YAMJ directory '%s' does not exist" % PYD_YAMJ_DIR )
    os.environ[ 'PYD_YAMJ_DIR' ] = PYD_YAMJ_DIR
    
    PYD_CLEAN_OUT_DIR = config.getboolean( MYSELF, 'clean.output.dir' )
    
    PYD_THEME_DIR = config.get( themeSectionName, 'theme.dir' )
    PYD_THEME_DIR = os.path.abspath( os.path.normpath( os.path.join( PYD_THEME_DIR, PYD_THEME ) ) )
    if not os.path.exists( PYD_THEME_DIR ):
        error( "Theme directory '%s' does not exist" % PYD_THEME_DIR )
    os.environ[ 'PYD_THEME_DIR' ] = PYD_THEME_DIR
    
    PYD_TPL_DIR = os.path.join( PYD_THEME_DIR, 'template' )
    if not os.path.exists( PYD_TPL_DIR ):
        error( "Template directory '%s' does not exist" % PYD_TPL_DIR )
    os.environ[ 'PYD_TPL_DIR' ] = PYD_TPL_DIR
    
    PYD_IMAGE_DIR = os.path.join( PYD_THEME_DIR, 'image' )
    if not os.path.exists( PYD_IMAGE_DIR ):
        error( "Image directory '%s' does not exist" % PYD_IMAGE_DIR )
    os.environ[ 'PYD_IMAGE_DIR' ] = PYD_IMAGE_DIR
    
    PYD_SCRIPTS_DIR = os.path.join( PYD_THEME_DIR, 'script' )
    if not os.path.exists( PYD_SCRIPTS_DIR ):
        error( "Scripts directory '%s' does not exist" % PYD_SCRIPTS_DIR )
    os.environ[ 'PYD_SCRIPTS_DIR' ] = PYD_SCRIPTS_DIR
    
    PYD_LOCALE_DIR = os.path.join( PYD_THEME_DIR, 'locale' )
    if not os.path.exists( PYD_LOCALE_DIR ):
        error( "Locale directory '%s' does not exist" % PYD_LOCALE_DIR )
    os.environ[ 'PYD_LOCALE_DIR' ] = PYD_LOCALE_DIR
	
    PYD_CAT_DUFO_TPL = config.get( templateSectionName, 'category.dune.folder.templ' )
    PYD_CAT_DUFO_TPL = os.path.join( PYD_TPL_DIR, PYD_CAT_DUFO_TPL )
    if not os.path.exists( PYD_CAT_DUFO_TPL ):
        error( "Category template ('%s') does not exist" % PYD_CAT_DUFO_TPL )
    os.environ[ 'PYD_CAT_DUFO_TPL' ] = PYD_CAT_DUFO_TPL
    
    PYD_SUBCAT_DUFO_TPL = config.get( templateSectionName, 'subcategory.dune.folder.templ' )
    PYD_SUBCAT_DUFO_TPL = os.path.join( PYD_TPL_DIR, PYD_SUBCAT_DUFO_TPL )
    if not os.path.exists( PYD_SUBCAT_DUFO_TPL ):
        error( "Subcategory template ('%s') does not exist" % PYD_SUBCAT_DUFO_TPL)
    os.environ[ 'PYD_SUBCAT_DUFO_TPL' ] = PYD_SUBCAT_DUFO_TPL
    
    PYD_TL_DUFO_TPL = config.get( templateSectionName, 'TL.Dune.Folder.Templ' )
    PYD_TL_DUFO_TPL = os.path.join( PYD_TPL_DIR, PYD_TL_DUFO_TPL )
    if not os.path.exists( PYD_TL_DUFO_TPL ):
        error( "Top-level template ('%s') does not exist" % PYD_TL_DUFO_TPL )
    os.environ[ 'PYD_TL_DUFO_TPL' ] = PYD_TL_DUFO_TPL
    
    PYD_MOVIE_DUFO_TPL = config.get( templateSectionName, 'movie.dune.folder.templ' )
    PYD_MOVIE_DUFO_TPL = os.path.join( PYD_TPL_DIR, PYD_MOVIE_DUFO_TPL )
    if not os.path.exists( PYD_MOVIE_DUFO_TPL ):
        error( "Movie template ('%s') does not exist" % PYD_MOVIE_DUFO_TPL )
    os.environ[ 'PYD_MOVIE_DUFO_TPL' ] = PYD_MOVIE_DUFO_TPL
    
    PYD_MOVIESET_DUFO_TPL = config.get( templateSectionName, 'movieset.dune.folder.templ' )
    PYD_MOVIESET_DUFO_TPL = os.path.join( PYD_TPL_DIR, PYD_MOVIESET_DUFO_TPL )
    if not os.path.exists( PYD_MOVIESET_DUFO_TPL ):
        error( "Movie set template ('%s') does not exist" % PYD_MOVIESET_DUFO_TPL )
    os.environ[ 'PYD_MOVIESET_DUFO_TPL' ] = PYD_MOVIESET_DUFO_TPL

    PYD_TVSET_DUFO_TPL = config.get( templateSectionName, 'tvset.dune.folder.templ' )
    PYD_TVSET_DUFO_TPL = os.path.join( PYD_TPL_DIR, PYD_TVSET_DUFO_TPL )
    if not os.path.exists( PYD_TVSET_DUFO_TPL ):
        error( "TV set template ('%s') does not exist" % PYD_TVSET_DUFO_TPL )
    os.environ[ 'PYD_TVSET_DUFO_TPL' ] = PYD_TVSET_DUFO_TPL
    
    PYD_BCKGR_IMAGE = config.get( imageSectionName, 'default.background.image' )
    PYD_BCKGR_IMAGE = os.path.join( PYD_IMAGE_DIR, PYD_BCKGR_IMAGE )
    if not os.path.exists( PYD_BCKGR_IMAGE ):
        error( "Background image '%s' does not exist" % PYD_BCKGR_IMAGE )
    os.environ[ 'PYD_BCKGR_IMAGE' ] = PYD_BCKGR_IMAGE
    
    PYD_LOGO_IMAGE = config.get( imageSectionName, 'logo.image' )
    PYD_LOGO_IMAGE = os.path.join( PYD_IMAGE_DIR, PYD_LOGO_IMAGE )
    if not os.path.exists( PYD_LOGO_IMAGE ):
        error( "Logo image '%s' does not exist" % PYD_LOGO_IMAGE )
    os.environ[ 'PYD_LOGO_IMAGE' ] = PYD_LOGO_IMAGE
    
    PYD_ICON_MASK = config.get( imageSectionName, 'icon.mask' )
    PYD_ICON_CAT_MASK = config.get( imageSectionName, 'icon.category.mask' )
    
    PYD_ICON_FILE = PYD_ICON_MASK % ""
    PYD_ICON_CAT_FILE = PYD_ICON_CAT_MASK % ""
    
    os.environ[ 'PYD_ICON_FILE' ] = PYD_ICON_FILE
    os.environ[ 'PYD_ICON_CAT_FILE' ] = PYD_ICON_CAT_FILE
    
    PYD_ICON_THUMB_FILE = PYD_ICON_MASK % "_thumb"
    os.environ[ 'PYD_ICON_THUMB_FILE' ] = PYD_ICON_THUMB_FILE
    
    PYD_ICON_SEL_FILE = PYD_ICON_MASK % "_sel"
    os.environ[ 'PYD_ICON_SEL_FILE' ] = PYD_ICON_SEL_FILE
    
    PYD_ICON_CAT_SEL_FILE = PYD_ICON_CAT_MASK % "_sel"
    os.environ[ 'PYD_ICON_CAT_SEL_FILE' ] = PYD_ICON_CAT_SEL_FILE
    
    PYD_ICON_USE_SEL = config.getboolean( imageSectionName, 'icon.use.selected' )
    os.environ[ 'PYD_ICON_USE_SEL' ] = str(PYD_ICON_USE_SEL)
    
    PYD_LANG = config.get( MYSELF, 'language' )
    os.environ[ 'PYD_LANG' ] = PYD_LANG
    
    try:
        PYD_ICON_WIDTH = config.getint( imageSectionName, 'icon.width' )
    except ValueError:
        log.warning( "Icon width in configuration file is NOT an integer, using default: %d" % PYD_ICON_WIDTH)
    if PYD_ICON_WIDTH < 0:
        error( "Icon width must be greater than 0" )
    os.environ[ 'PYD_ICON_WIDTH' ] = str(PYD_ICON_WIDTH)
    
    try:
        PYD_ICON_HEIGHT = config.getint( imageSectionName, 'icon.height' )
    except ValueError:
        log.warning( "Icon height in configuration file is NOT an integer, using default: %d" % PYD_ICON_HEIGHT )
    if PYD_ICON_HEIGHT < 0:
        error( "Icon height must be greater than 0" )
    os.environ[ 'PYD_ICON_HEIGHT' ] = str(PYD_ICON_HEIGHT)
    
    try:
        PYD_ICON_CATEGORY_WIDTH = config.getint( imageSectionName, 'icon.category.width' )
    except ValueError:
        log.warning( "Category icon width in configuration file is NOT an integer, using default: %d" % PYD_ICON_CATEGORY_WIDTH )
    if PYD_ICON_CATEGORY_WIDTH < 0:
        error( "Category icon width must be greater than 0" )
    os.environ[ 'PYD_ICON_CATEGORY_WIDTH' ] = str(PYD_ICON_CATEGORY_WIDTH)
    
    try:
        PYD_ICON_CATEGORY_HEIGHT = config.getint( imageSectionName, 'icon.category.height' )
    except ValueError:
        log.warning( "Category icon height in configuration file is NOT an integer, using default: %d" % PYD_ICON_CATEGORY_HEIGHT )
    if PYD_ICON_CATEGORY_HEIGHT < 0:
        error( "Category icon height must be greater than 0" )
    os.environ[ 'PYD_ICON_CATEGORY_HEIGHT' ] = str(PYD_ICON_CATEGORY_HEIGHT)
    
    PYD_ICON_DEFAULT = os.path.join( PYD_IMAGE_DIR, PYD_ICON_MASK % "_default_%sx%s" % (PYD_ICON_WIDTH, PYD_ICON_HEIGHT) )
    if not os.path.exists( PYD_ICON_DEFAULT ):
        error( "Default icon '%s' does not exist" % PYD_ICON_DEFAULT )
    os.environ[ 'PYD_ICON_DEFAULT' ] = PYD_ICON_DEFAULT
    
    try:
        PYD_ICON_SCALE_FACTOR = config.getfloat( imageSectionName, 'icon.scale.factor' )
    except ValueError:
        log.warning( "Icon scale factor in configuration file is NOT a float, using default: %0.3f" % PYD_ICON_SCALE_FACTOR )
    if PYD_ICON_SCALE_FACTOR <= 0.0:
        error( "Icon scale factor must be greater than 0" )
    os.environ[ 'PYD_ICON_SCALE_FACTOR' ] = str(PYD_ICON_SCALE_FACTOR)

    try:
        PYD_TVICON_SCALE_FACTOR = config.getfloat( imageSectionName, 'icon.tvepisode.scale.factor' )
    except ValueError:
        log.warning( "TV icon scale factor in configuration file is NOT a float, using default: %0.3f" % \
            PYD_TVICON_SCALE_FACTOR )
    if PYD_TVICON_SCALE_FACTOR <= 0.0:
        error( "TV icon scale factor must be greater than 0" )
    os.environ[ 'PYD_TVICON_SCALE_FACTOR' ] = str(PYD_TVICON_SCALE_FACTOR)
    
    PYD_SCR_MAKE_CAT_ICON = config.get( scriptSectionName, 'script.make.category.icon' )
    PYD_SCR_MAKE_CAT_ICON = os.path.join( PYD_SCRIPTS_DIR, PYD_SCR_MAKE_CAT_ICON)
    if not os.path.exists( PYD_SCR_MAKE_CAT_ICON ):
        error( "Script '%s' for making category icon does not exist" % PYD_SCR_MAKE_CAT_ICON )
    if not os.path.isfile( PYD_SCR_MAKE_CAT_ICON ):
        error( "Script '%s' must be a file" % PYD_SCR_MAKE_CAT_ICON )
    
    PYD_SCR_MAKE_BCKGR_IMAGE = config.get( scriptSectionName, 'script.make.background.image' )
    PYD_SCR_MAKE_BCKGR_IMAGE = os.path.join( PYD_SCRIPTS_DIR, PYD_SCR_MAKE_BCKGR_IMAGE)
    if not os.path.exists( PYD_SCR_MAKE_BCKGR_IMAGE ):
        error( "Script '%s' for making movie background image does not exist" % PYD_SCR_MAKE_BCKGR_IMAGE )
    if not os.path.isfile( PYD_SCR_MAKE_BCKGR_IMAGE ):
        error( "Script '%s' must be a file" % PYD_SCR_MAKE_BCKGR_IMAGE )
        
    PYD_SCR_MAKE_THUMB_IMAGE = config.get( scriptSectionName, 'script.make.thumbnail.image' )
    PYD_SCR_MAKE_THUMB_IMAGE = os.path.join( PYD_SCRIPTS_DIR, PYD_SCR_MAKE_THUMB_IMAGE)
    if not os.path.exists( PYD_SCR_MAKE_THUMB_IMAGE ):
        error( "Script '%s' for making thumbnail images does not exist" % PYD_SCR_MAKE_THUMB_IMAGE )
    if not os.path.isfile( PYD_SCR_MAKE_THUMB_IMAGE ):
        error( "Script '%s' must be a file" % PYD_SCR_MAKE_THUMB_IMAGE )
        
    PYD_SCR_MAKE_PART_THUMB = config.get( scriptSectionName, 'script.make.part.thumbnail' )
    PYD_SCR_MAKE_PART_THUMB = os.path.join( PYD_SCRIPTS_DIR, PYD_SCR_MAKE_PART_THUMB )
    if not os.path.exists( PYD_SCR_MAKE_THUMB_IMAGE ):
        error( "Script '%s' for making thumbnail for movie parts does not exist" % PYD_SCR_MAKE_PART_THUMB )
    if not os.path.isfile( PYD_SCR_MAKE_PART_THUMB ):
        error( "Script '%s' must be a file" % PYD_SCR_MAKE_PART_THUMB )
        
    PYD_SCR_MAKE_EP_THUMB = config.get( scriptSectionName, 'script.make.episode.thumbnail' )
    PYD_SCR_MAKE_EP_THUMB = os.path.join( PYD_SCRIPTS_DIR, PYD_SCR_MAKE_EP_THUMB )
    if not os.path.exists( PYD_SCR_MAKE_EP_THUMB ):
        error( "Script '%s' for making episode thumbnails does not exist" % PYD_SCR_MAKE_EP_THUMB )
    if not os.path.isfile( PYD_SCR_MAKE_EP_THUMB ):
        error( "Script '%s' must be a file" % PYD_SCR_MAKE_EP_THUMB )
        
    PYD_SCR_MAKE_MOVIE_ICON = config.get( scriptSectionName, 'script.make.movie.icon' )
    PYD_SCR_MAKE_MOVIE_ICON = os.path.join( PYD_SCRIPTS_DIR, PYD_SCR_MAKE_MOVIE_ICON )
    if not os.path.exists( PYD_SCR_MAKE_MOVIE_ICON ):
        error( "Script '%s' for making movie icons does not exist" % PYD_SCR_MAKE_MOVIE_ICON )
    if not os.path.isfile( PYD_SCR_MAKE_MOVIE_ICON ):
        error( "Script '%s' must be a file" % PYD_SCR_MAKE_MOVIE_ICON )
### end checkConfig ###


def init():
    global PYD_CONFIG_FILE
    
    if not PYD_CONFIG_FILE:
        error( "Configuration file not defined", 3 )
    if not os.path.exists( PYD_CONFIG_FILE ):
        error( "Configuration file '%s' does not exist" % PYD_CONFIG_FILE, 4 )
    
    config = ConfigParser.SafeConfigParser( CONFIG_DEFAULTS )
    config.readfp( open( PYD_CONFIG_FILE ), "r" )
    
    checkConfig( config )


def debug():
    log.debug( "Log file = %s" % PYD_LOG_FILE )
    log.debug( "Output directory = %s" % PYD_OUT_DIR )
    log.debug( "YAMJ directory = %s" % PYD_YAMJ_DIR )
    log.debug( "YAMJ directory after normalisation = %s" % PYD_YAMJ_DIR )
    log.debug( "Clean output directory = %s" % PYD_CLEAN_OUT_DIR )
    log.debug( "Language = %s" % PYD_LANG ) 
    log.debug( "Theme directory = %s" % PYD_THEME_DIR )
    log.debug( "Template directory = %s" % PYD_TPL_DIR )
    log.debug( "Image directory = %s" % PYD_IMAGE_DIR )
    log.debug( "Locale directory = %s" % PYD_LOCALE_DIR )
    log.debug( "Category dune_folder.txt template = %s" % PYD_CAT_DUFO_TPL )
    log.debug( "Subcategory dune_folder.txt template = %s" % PYD_SUBCAT_DUFO_TPL )
    log.debug( "Top-level dune_folder.txt template = %s" % PYD_TL_DUFO_TPL )
    log.debug( "Movie dune_folder.txt template = %s" % PYD_MOVIE_DUFO_TPL )
    log.debug( "Movie set dune_folder.txt template = %s" % PYD_MOVIESET_DUFO_TPL )
    log.debug( "TV set dune_folder.txt template = %s" % PYD_TVSET_DUFO_TPL )
    log.debug( "Background image = %s" % PYD_BCKGR_IMAGE )
    log.debug( "Logo image = %s" % PYD_LOGO_IMAGE )
    log.debug( "Icon file name = %s" % PYD_ICON_FILE )
    log.debug( "Icon category file name = %s" % PYD_ICON_CAT_FILE )
    log.debug( "File for selected icon = %s" % PYD_ICON_SEL_FILE )
    log.debug( "File for selected category icon = %s" % PYD_ICON_CAT_SEL_FILE )
    log.debug( "Default icon = %s" % PYD_ICON_DEFAULT )
    log.debug( "Thumbnail icon file name = %s" % PYD_ICON_THUMB_FILE )
    log.debug( "Separated 'selected' icon will be used = %s" % PYD_ICON_USE_SEL )
    log.debug( "Icon width = %d pixels" % PYD_ICON_WIDTH )
    log.debug( "Icon height = %d pixels" % PYD_ICON_HEIGHT )
    log.debug( "Icon category width = %d pixels" % PYD_ICON_CATEGORY_WIDTH )
    log.debug( "Icon category height = %d pixels" % PYD_ICON_CATEGORY_HEIGHT )
    log.debug( "Icon scale factor = %0.3f" % PYD_ICON_SCALE_FACTOR )
    log.debug( "TV icon scale factor = %0.3f" % PYD_TVICON_SCALE_FACTOR )
    log.debug( "Scripts directory = %s" % PYD_SCRIPTS_DIR )
    log.debug( "Script for making category icon = %s" % PYD_SCR_MAKE_CAT_ICON )
    log.debug( "Script for making thumbnail images = %s" % PYD_SCR_MAKE_THUMB_IMAGE )
    log.debug( "Script for making background images = %s" % PYD_SCR_MAKE_BCKGR_IMAGE )
    log.debug( "Script for making thumbnail for movie part = %s" % PYD_SCR_MAKE_PART_THUMB )
    log.debug( "Script for making TV episode thumbnails = %s" % PYD_SCR_MAKE_EP_THUMB )
    log.debug( "Script for making movie icon = %s" % PYD_SCR_MAKE_MOVIE_ICON )
    log.debug( " " )
