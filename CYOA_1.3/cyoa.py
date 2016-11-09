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

        #currently this will not run as no output has been created
        #this sets the basic structure of the CYOA tool
        #version V1.1 end

        counter = 1
        #looping to check all the lines in raw_body
        for line in raw_body:
            unparsed_line = line
            parsed_line = ""
            while True:
                #reading both parsed and unparsed lines
                pre, mid, post = unparsed_line.partition("[[")
                if mid =="":
                    parsed_line += unparsed_line
                    break
                else:
                    link, mid2,post2 = post.partition("]]")
                    if mid2 =="":
                        parsed_line += unparsed_line
                        break
                    else:
                        self.links.append(parse_link(link))
                        unparsed_line = post2
                        parsed_line += pre
                        parsed_line += "("
                        # counting strings that are already parsed
                        parsed_line += str(counter)
                        parsed_line += ")"
                        counter += 1
                        #if not read
                        #add the already parsed lines
            while len(self.body) < 2 and not (parsed_line ==""):
                self.body.append("")
            self.body.append(parsed_line)

            if not (self.body[-1] == ""):
                self.body.append("")

                # sets the parameter in which lines in a file are being read
                #CYOA v1.2 complete
# def new game file class
#contains all attributes previously found in page class
class GameFile:
    def _init_(self, game_files, data):
        self.game_files = game_files
        self.raw_data = data
        self.pages = []
        self.page_dict = {}

#empty current page
        cur_page = []
        cur_page_name = None
        for line in data:
            #current page can be seperated and defined with the use of column []
            #when used in the imported text
            if len(line) >= 2 and line[0] == '[' and line [-1] == ']':
                if not(cur_page_name is None):
                    page = Page(self, cur_page_name, cur_page)
                    self.pages.append(page)
                    self.page_dict(cur_page_name) = page
                cur_page_name = line[1:-1]
                cur_page = []
            else:
                cur_page.append(line)

        if not (cur_page_name is None):
            page = Page(self, cur_page_name, cur_page)
            self.pages.append(page)
            self.page_dict[cur_page_name] = page

        if len(self.pages) > 0:
            self.page_dict[""] = self.pages[0]

        # Now the programme will go through all the pages in the import file to verify that there are no missing links
        # CYOA v1.3 complete
        #current problem: line self.page_dict(cur_page_name) = page
        # syntax error, can't assign to function call
                
                        
                        
                    
                
                


