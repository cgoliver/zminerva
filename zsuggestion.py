"""
Course Suggester

This script takes your list of all courses you would ever want to take, finds out which are available for a given semester, and presents them in order according to your priorities.

The <filename> argument is something like "courses.csv", which is a tab delimited file with columns "department", "code", and "priority". This is where you list the courses you want and how high priority they are to you.

The point here is to see whether the classes even exist for a given semester, not whether they have free spots.

Usage:
  zsuggestion.py <mcgill-user> <mcgill-pw> <filename> <season> <year> [options]
  
Options:
  --show-all      Shows all courses, even if they are inactive or not found.      
  
  -h --help       Show this screen.
  -v --version    Show version.
"""

import os.path

from docopt import docopt
from suggestion_manager import SuggestionManager
from zconstants import *
        
def main(args):
    if args["<season>"] not in SEASONS:
        print("Aborted: Invalid season: %s"%args["<season>"])
        return
    
    try:
        year=int(args["<year>"])
    except:
        print("Aborted: Invalid year: %s"%args["<year>"])
        return
    
    filename=args["<filename>"]
    if not os.path.isfile(filename):
        print("Aborted: File not found: %s"%filename)
        return
    
    sm=SuggestionManager(username=args["<mcgill-user>"],
                         password=args["<mcgill-pw>"],
                         filename=filename,
                         season=args["<season>"],
                         year=year)
    sm.show(show_all=args["--show-all"])    

if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    main(args)
















