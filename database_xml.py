import xml.sax as ss
# simple api for xml

# we need a handler that handles the xml file 
# and the parser that converts the tags into the python script

class GroupHandler(ss.ContentHandler):

    def startElement(self, lastmod, attrs):
        self.user = lastmod
        if self.user == '2021-05-12':
            print('change frequency: {}'.format(attrs['changefreq']))
    
handler = GroupHandler()
parser = ss.make_parser()
parser.setContentHandler(handler)
parser.parse('sitemap.xml')