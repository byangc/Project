#CYOA Tool
# allows access to system specific parameters and functions 
import sys

#Parse link using a specification based on the Python format () syntax
#Format: filename & Pagename strip using |
def parse_link(link):
    filename, _, pagename = link.rpartition ('|')
    return (filename.strip(), pagename.strip())

#defines class page to open up a page based on pagename
class Page:
    def _init_(self, game_file, pagename, raw_body):
        #assignment of variables
        self.game_file = game_file
        self.pagename = pagename
        self.raw_body = raw_body
        self.body = []
        self.links = []

        # currently this will not run as no output has been created
        # this sets the basic structure of the CYOA tool
        #version V1.1


