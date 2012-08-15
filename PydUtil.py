
import pydisconf


def copyTemplateFile( aFileSrc, aFileDst ):
    try:
        inFile = open( aFileSrc, 'r' )
    except IOError:
        pydisconf.error( "Cannot open input file '%s'" % aFileSrc )
    
    try:
        outFile = open( aFileDst, 'w' )
    except IOError:
        pydisconf.error( "Cannot open output file '%s'" % aFileDst )
        
    inList = inFile.readlines()
    outFile.writelines( inList )
    inList = []
    
    # Append lines for icon and selected icon
    inList.append( "# Added by PydUtil.copyTemplateFile" )
    inList.append( "icon_path = %s" % pydisconf.PYD_ICON_FILE )
    if pydisconf.PYD_ICON_USE_SEL:
        inList.append( "icon_sel_path = %s" % pydisconf.PYD_ICON_SEL_FILE )
    inList.append( "storage_caption = %s" % pydisconf.MYSELF )
    inList.append( "system_files = *.aai,*.jpg,*.png,*.gif,Library" )
    # Last item must have "\n" character because more items can be appended
    inList.append( "optimize_full_screen_background = yes\n" )
    
    outFile.write( "\n".join(inList) )
    
    inFile.close()
    outFile.close()
    pydisconf.debugText( "Copied '%s' to '%s'" % ( aFileSrc, aFileDst ) )
### copyTemplateFile ###
