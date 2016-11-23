#CYOA Tool
# allows access to system specific parameters and functions 
import sys
#Parse link using a specification based on the Python format () syntax
#Format: filename & Pagename strip using |
def parse_link(link):
    filename, _, pagename = link.rpartition('|')
    return (filename.strip(), pagename.strip())
#defines class page to open up a page based on pagename
#using _init_ method to allows for an flexible argument implementation
class Page:
    def __init__(self, game_file, pagename, raw_body):
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
                if mid == "":
                    parsed_line += unparsed_line
                    break
                else:
                    link, mid2, post2 = post.partition("]]")
                    if mid2 == "":
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
            while len(self.body) < 2 and not (parsed_line == ""):
                self.body.append("")
                # sets the parameter in which lines in a file are being read
                #CYOA v1.2 complete
                # def new game file class
                #contains all attributes previously found in page class
            self.body.append(parsed_line)

        if not (self.body[-1] == ""):
            self.body.append("")

class GameFile:
    def __init__(self, game_files, data):
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
            if len(line) >= 2 and line[0] == '[' and line[-1] == ']':
                if not (cur_page_name is None):
                    page = Page(self, cur_page_name, cur_page)
                    self.pages.append(page)
                    self.page_dict[cur_page_name] = page
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
        # Error fixed, due to typography caused by confusion of lower and upper cases
        for page in self.pages:
            for filename, pagename in page.links:
                if filename == "" and not (pagename in self.page_dict):
                    print ("Missing page \"" + pagename + "\".")
# define get page class
# obtaining pagename if none found return cannot find the page
    def get_page(self, pagename):
        page = self.page_dict.get(pagename)
        if page is None:
            print ("Cannot find page \"" + pagename + "\".")
        return page

class GameFiles:
    def __init__(self):
        self.files = []
        self.file_dict = {}
#created load_file method to allow file to be opened
    def load_file(self, filename):
        if not (filename in self.file_dict):
            try:
                f = open(filename)
                data = f.readlines()
                f.close()

                #Following code are used to trim extraneous endlines
                data2 = []
                for line in data:
                    data2.append(line[:-1])

                game_file = GameFile(self, data2)
                self.files.append(game_file)
                self.file_dict[filename] = game_file
                #finally in python make sure files or resources are closed or released regardless of whether an exception occurs
            finally:
                #pass is null operation, nothing will happen when it executes
                pass

    # If the game file is not found the programe will return 'None'.
    #message indicate that file cannot be located
    def get_game_file(self, filename):
        self.load_file(filename)
        return self.file_dict.get(filename)

    def get_page(self, filename, pagename):
        game_file = self.get_game_file(filename)
        if game_file is None:
            print ("Cannot find file \"" + filename + "\".")
            return None
        return game_file.get_page(pagename)

    #CYOAv1.4 complete

# Returns
#Quit program displayed if player wants to quit the CYOA tool
#Previous page displayed if the player wants to go back to previous page

quit_program = object()
previous_page = object()

class TextDisplay:
    def __init__(self, page_size = 50):
        self.page_size = page_size

    def start(self):
        pass

    def end(self):
        pass

   # The following code will display to the user as a menu which helps with the navigation of the tool
   # Returns
   # p - if the player wants to go to a specific page 'p'
   #
   # User types a number 'p' to go to that page
   #
   # User input returns
   #user can type 'back' to go to the previous page
   #user can type 'exit' or 'quit' to exit the program
   #User can type 'help' to go to the help page which provides simple instruction on the use of the tool
   #User can type 'refresh' to display the prompt again in case the previous message was not read
    def display_page(self, page):
        def link_index(i):
            game_file = page.game_file
            filename, pagename = page.links[i - 1]
            # filename can be returned or entered by the user either as the page name or the name of the file
            if filename == "":
                return game_file.get_page(pagename)
            else:
                return game_file.game_files.get_page(filename, pagename)

        while True:

            #while the condition is true
            #for loop checking against the page body and page size so that it is equal to 0
            #start from beginning
            for i in range(0, len(page.body)):
                if i > 0 and i + 1 < len(page.body) and (i % self.page_size) == 0:
                    # user prompted to press enter to continue
                    try:
                        input ("[[Press enter to continue.]]")
                        # with the exception that if nothing is showing the program will be terminated
                    except:
                        print ("")
                        return quit_program
                print (page.body[i])

                # exception for when the input is >
                # nothing is returned and thus the program is terminated

            while True:
                try:
                    choice = input ("> ")
                except:
                    print ("")
                    return quit_program
    #Return none if the choice is blank == 0
                if len(choice) == 0:
                    if len(page.links) == 1:
                        new_page = link_index(1)
                        if not (new_page is None):
                            return new_page
                        # When choice is 'r' for refresh the text
                elif choice[0] == 'r':
                    break
                # When choice is 'b' for back to the previous page
                elif choice[0] == 'b':
                    return previous_page
                # When choice is 'q' for quitting the program and choice is 'e' for exit program
                # return quit_program
                elif choice[0] == 'q' or choice[0] == 'e':
                    return quit_program

                # When the choice is 'h' for help, bring up the help page from the games folder
                # help page will be displayed as a new page
                elif choice[0] == 'h':
                    game_files = page.game_file.game_files
                    new_page = game_files.get_page("games/help", "")
                    return new_page

                # CYOA v1.5 complete
                # No Error occurred

                # ensure that the choice is a digit
                elif choice.isdigit():
                    i = int(choice)
                # the choice must be greater than or equal to 1
                # cannot be choice 0
                # The choice must be the ones specified in the page links
                # e.g. if page link has choice 5, player will not be able to choose option 6
                    if i >= 1 and i <= len(page.links):
                        new_page = link_index(i)
                        if not (new_page is None):
                            return new_page
                        # Messages according to user input
                    else:
                        # select 0 = no such choice, seek alternatives
                        if len(page.links) == 0:
                            print ("There are no choices. Type \"back\" to go back, \"quit\" to quit, or \"help\" for help.")
                        # select 1 is unavailable due to it being the only choice so no selection is required
                        elif len(page.links) == 1:
                            print ("Choice " + choice + " is unavailable. This is only one choice. (Pressing 'enter' will continue with the only choice.)")
                       # when the selected option is not explicitly created by the user or none existent     
                        else:
                            print ("Choice " + choice + " is unavailable. There are only " + str(len(page.links)) + " choices.")
                      # When the selected option is not in the correct format e.g. user input one instead of 1      
                else:
                    print ("I did not understand \"" + choice + "\". Type \"help\" for help.")
                    # minor error occurred in the indentation
        # fixed by indenting twice
        return quit_program

def main_loop(display, start_page):
    #begin to show the start page
    display.start()
    # start page is shown as the last viewed page (aka page history)
    page_history = [start_page]

    while True:
        cur_page = page_history[-1]
        # next page displays new page according to page history -1
        next_page = display.display_page(cur_page)
        # next page = quit then break
        if next_page is quit_program:
            break
        # or else pop or remove the item at the given position in the list (removes and returns the last item in the list)
        elif next_page is previous_page:
            if len(page_history) > 1:
                page_history.pop()
        else:
            # add page history to the end of the list
            page_history.append(next_page)

    display.end()
# main() function makes it possible to run the code with import module
# execute source line by line
def main():
    # sys.argv
    # The list of command line arguments passed to a python script
    # to loop over the stadard input or list of files given on the command line
    num_args = len(sys.argv) - 1

    if num_args == 0:
        filename = "menu"
        pagename = ""
    elif num_args == 1:
        filename = sys.argv[1]
        pagename = ""
    elif num_args == 2:
        filename = sys.argv[1]
        pagename = sys.argv[2]

    game_files = GameFiles()

    main_loop(TextDisplay(), game_files.get_page(filename, pagename))

main()
#Core program complete
#CYOA v2.1
