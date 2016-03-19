"""
Minerva Crawler

Regularly logs into McGill's Minerva website to check if courses you want are open. If their statuses change, it sends you an email.

Usage:
  zminerva.py <mcgill-user> [options]
  zminerva.py <mcgill-user> <recipient> <gmail-user> [options]

Options:
  --interval=<minutes>   Wait this number of minutes after finishing a search before starting another. [default: 30]
  --verbose              Extra output will print to console and save to the logs.
  --report=<days>        zminerva will send an email update even if there are no course status changes. Set the number of days between each report. [default: 0]
  
  -h --help           Show this screen.
  -v --version        Show version.
"""

import os.path, re, getpass
from docopt import docopt
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

def create_demo_watchlist():    
    example="""#Demo watchlist file. List as many classes as you want to monitor.
#If a course status keeps showing up as unknown, maybe the semester, 
#department, code, or crn are wrong. Lines starting with "#" are ignored.
#You can change this file while zminerva is running.
fall 2013,comp 201

#You can also be more specific by adding a CRN like so:
winter 2014,edpe 301,crn 1337"""
    with open("watchlist","w") as f:
        f.write(example)
    
    print("Created demo watchlist file. Open the file \"watchlist\" in the zminerva directory to see a working example.")

def main(args):
    try:
        interval=int(args["--interval"])
        interval=5 if interval<5 else interval
    except:
        print("Abort: Invalid interval: %s"%args["--interval"])
        return
    
    if args["<gmail-user>"] and "@gmail.com" not in args["<gmail-user>"]:
        print("Abort: Invalid email: %s. The sender of the emails must be a gmail account."%args["<gmail-user>"])
        return
    
    watchlist=get_watchlist()
    if not watchlist:
        print("Abort: Failed to find watchlist.")
        create_demo_watchlist()
        return
    
    try:
        report_days=int(args["--report"])
    except:
        print("Abort: Invalid value for report days: %s"%args["--report"])
        return

    mcgill_pw=getpass.getpass("Enter the password for '%s':"%args["<mcgill-user>"])
    gmail_pw=""
    if args["<gmail-user>"]:
        gmail_pw=getpass.getpass("Enter the password for '%s':"%args["<gmail-user>"])
    
    ml=MinervaLoop(args["<mcgill-user>"],
                mcgill_pw,
                watchlist,
                interval=interval,
                gmail_user=args["<gmail-user>"],
                gmail_pw=gmail_pw,
                gmail_recipient=args["<recipient>"],
                verbose=args["--verbose"],
                report_days=report_days,
                args=args)

if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    main(args)
















