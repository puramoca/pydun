import xml.sax

# Procedure division


class PydCategoryParser(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.toDebug = None
        self.currData = None
        self.currElem = None
        self.categories = {}
        self.name = None
        self.originalName = None
        self.category = None
        
    def debug(self, arg):
        print "(D-category-parser): " + str(arg).encode('utf-8')
        
    def startElement(self, name, attrs):
        self.currElem = name
        if name == 'category':
            if attrs.has_key( 'name' ):
                self.categories[ attrs[ 'name' ] ] = []
            self.category = attrs[ 'name' ]
        elif name == 'index':
            if attrs.has_key( 'name' ):
                self.name = unicode(attrs[ 'name' ])
            if attrs.has_key( 'originalName' ):
                self.originalName = attrs[ 'originalName' ].encode('utf-8')
    
    def endElement(self, name):
        if name == 'index':
            self.categories[ self.category ].append( (self.name, self.originalName, self.currData) )
            
    def characters(self, data):
        self.currData = xml.sax.saxutils.escape(data)
        if self.currElem == 'index':
            rightUnderscore = self.currData.rfind('_')
            if rightUnderscore > -1:
                self.currData = self.currData[:rightUnderscore+1] + '*.xml'
### PydCategoryParser ###

