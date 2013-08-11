"""
Minerva Crawl

Usage:
  mcrawl.py <mcgill-user> <mcgill-pw> [<gmail-recipient> <gmail-user> <gmail-pw>] [options]

Options:
  --interval=<i>      Wait this number of seconds after finishing a search before starting another. [default: 300]
  --verbose           Print lots of info to console.
  --headless          Necessary on commandline servers. Runs firefox headless, meaning invisibly.
  
  -h --help           Show this screen.
  -v --version        Show version.
"""

import os.path, re, logging, datetime
from ztools.docopt import docopt
from minerva_loop import MinervaLoop

def get_log_name():
    dt=datetime.datetime.now()
    return "%s-%s-%s-mcrawl.log"%(dt.year,dt.month,dt.day)

def set_logger(verbose):
    logger = logging.getLogger("mcrawl")
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    fh = logging.FileHandler("logs/"+get_log_name())
    #fh.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    #ch.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

def get_watchlist():
    path="watchlist"
    if not os.path.isfile(path):
        logger = logging.getLogger("mcrawl")
        logger.critical("Failed to find file: %s"%path)
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
    logger=set_logger(args["--verbose"])
    try:
        interval=int(args["--interval"])
    except:
        logger.warning("Invalid interval: %s"%args["--interval"])
        interval=20
    
    watchlist=get_watchlist()
    if not watchlist:
        return
    
    print(args)
    
    ml=MinervaLoop(args["<mcgill-user>"],
                args["<mcgill-pw>"],
                watchlist,
                interval=interval,
                headless=args["--headless"],
                gmail_user=args["<gmail-user>"],
                gmail_pw=args["<gmail-pw>"],
                gmail_recipient=args["<gmail-recipient>"])

if __name__ == "__main__":
    args = docopt(__doc__, version="0.1")
    main(args)
















