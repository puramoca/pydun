
class PydMoviePart:
    
    def __init__(self):
        self.fileTitle = ''
        self.fileLocation = None
        self.firstAired = None
        self.filePlot = ''
        self.fileImageFile = None
        self.fileURL = None
        # Ordinal number of given part (episode or movie part)
        self.part = None

    def __repr__(self):
        retstr = "<PydMoviePart: fileTitle='%s', fileLocation=%s, fileURL=%s, firstAired='%s', part=%d, filePlot='%s', fileImageFile (videoimage)=%s>" % (self.fileTitle, self.fileLocation, self.fileURL, self.firstAired, self.part, self.filePlot, self.fileImageFile)
        return retstr
