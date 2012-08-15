
class PydMovie:
    
    def __init__(self):
        self.baseFilename = ''
        self.baseFilenameBase = ''
        self.title = ''
        self.originalTitle = ''
        self.year = ''
        self.releaseDate = ''
        # Array of ratings
        self.ratings = {}
        self.posterFile = ''
        self.detailPosterFile = ''
        self.fanartFile = ''
        self.thumbnail = ''
        self.bannerFile = ''
        self.clearlogoFile = ''
        self.clearartFile = ''
        self.tvthumbFile = ''
        self.plot = ''
        self.outline = ''
        self.quote = ''
        self.tagline = ''
        self.country = ''
        self.company = ''
        self.runtime = ''
        self.certification = ''
        self.language = ''
        self.subtitles = ''
        self.container = ''
        self.videoCodec = ''
        self.audioCodec = ''
        self.audioChannels = ''
        self.resolution = ''
        self.videoSource = ''
        self.videoOutput = ''
        self.aspect = ''
        self.fps = ''
        self.directors = []
        self.writers = []
        self.actors = []
        self.top250 = '251'
        self.isSet = None
        self.isTV = None
        self.set = None
        self.season = None
        # List containing data about episode files or parts files
        self.parts = []

    # Method that prints class
    def __repr__(self):
        retstr = "<PydMovie: title=%s, originalTitle=%s, baseFilename=%s, baseFilenameBase=%s, year=%s, releaseDate=%s, ratings=%s, posterFile=%s, detailPosterFile=%s, fanartFile=%s, thumbnail=%s, bannerFile=%s, clearlogoFile=%s, clearartFile=%s, tvthumbFile=%s, plot='%s', outline='%s', quote='%s', tagline='%s', country=%s, company=%s, runtime=%s, certification=%s, language=%s, subtitles=%s, container=%s, videoCodec=%s, audioCodec=%s, audioChannels=%s, resolution=%s, videoSource=%s, videoOutput=%s, aspect=%s, fps=%s, directors=%s, writers=%s, actors=%s, top250=%s, isSet=%s, isTV=%s, season=%s parts=%s, set=%s>" % (self.title, self.originalTitle, self.baseFilename, self.baseFilenameBase, self.year, self.releaseDate, self.ratings, self.posterFile, self.detailPosterFile, self.fanartFile, self.thumbnail, self.bannerFile, self.clearlogoFile, self.clearartFile, self.tvthumbFile, self.plot, self.outline, self.quote, self.tagline, self.country, self.company, self.runtime, self.certification, self.language, self.subtitles, self.container, self.videoCodec, self.audioCodec, self.audioChannels, self.resolution, self.videoSource, self.videoOutput, self.aspect, self.fps, self.directors, self.writers, self.actors, self.top250, self.isSet, self.isTV, self.season, self.parts, self.set)
        return retstr
# end class PydMovie

