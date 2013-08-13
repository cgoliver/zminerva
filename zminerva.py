"""
Minerva Crawl

Usage:
  mcrawl.py <mcgill-user> <mcgill-pw> [<recipient> <gmail-user> <gmail-pw>] [options]

Options:
  --interval=<i>      Wait this number of seconds after finishing a search before starting another. [default: 1800]
  --verbose           Extra output will print to console and save to the logs.
  --headless          Necessary on commandline servers. Runs firefox headless, meaning invisibly.
  
  -h --help           Show this screen.
  -v --version        Show version.
"""

import os.path, re
from ztools.docopt import docopt
from minerva_loop import MinervaLoop

def get_watchlist():
    path="watchlist"
    if not os.path.isfile(path):
        return list()
    
    with open(path,"r") as f:
        lines=f.readlines()
    
    lines=[line.strip().lower() for line in lines if line.strip() and line[0]!="#"]
    
    watchlist=[parse_watchline(line) for line in lines]
    return watchlist

def parse_watchline(line):
    pieces=re.split("[ \t]*,[ \t]*",line)
    
    item={"semester":"",
          "dep":"",
          "code":"",
          "crn":""}
    
    semesters=("winter","fall","summer")
    for piece in pieces:
        for semester in semesters:
            s_flag=0
            if not piece.find(semester):
                item["semester"]=piece
                s_flag=1
                continue
        if s_flag:
            continue
        
        if not piece.find("crn"):
            try:
                item["crn"]=int(re.split("[ ]+",piece)[1])
                continue
            except:
                pass
        
        try:
            dep,code=re.split("[ ]+",piece)
            item["dep"]=dep
            item["code"]=code
        except:
            pass
    
    item["depcode"]=item["dep"]+item["code"]
    return item

def main(args):
    try:
        interval=int(args["--interval"])
    except:
        print("Abort: Invalid interval: %s"%args["--interval"])
        return
    
    if "@gmail.com" not in args["<gmail-user>"]:
        print("Abort: Invalid email: %s. The sender of the emails must be a gmail account."%args["<gmail-user>"])
        return
    
    watchlist=get_watchlist()
    if not watchlist:
        print("Abort: Failed to find watchlist.")
        return
    
    ml=MinervaLoop(args["<mcgill-user>"],
                args["<mcgill-pw>"],
                watchlist,
                interval=interval,
                headless=args["--headless"],
                gmail_user=args["<gmail-user>"],
                gmail_pw=args["<gmail-pw>"],
                gmail_recipient=args["<recipient>"],
                verbose=args["--verbose"],
                args=args)

if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    main(args)
















