
import logging
from minerva_bot import MinervaBot

from zconstants import *

class SuggestionManager():
    def __init__(self,username,password,filename,season,year):
        self.username=username
        self.password=password
        self.filename=filename
        self.season=season
        self.year=year
        
        self.set_logger()
        self.set_courses()
        self.set_coursemanager()
        self.set_scores()
    
    def set_logger(self):
        self.logger = logging.getLogger("zsuggestion")
        self.logger.setLevel(logging.INFO)
        
        ch = logging.StreamHandler()
        
        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        
        self.logger.handlers=[]
        self.logger.addHandler(ch)
    
    def get_departments(self):
        deps=[course["dep"].upper() for course in self.courses]
        return set(deps)
    
    def set_coursemanager(self):
        
        mb=MinervaBot(self.username,self.password,logger=self.logger)
        
        semester="%s %s"%(self.season,self.year)
                
        self.cm=mb.get_course_manager(semester,
                                      self.get_departments())
        
    def set_courses(self):
        with open(self.filename,"r") as f:
            lines=f.read().split("\n")
            
        self.courses=[]
        
        for line in lines[1:]:
            if not line.strip():
                continue
            
            split=line.split("\t")
            if len(split)<3:
                continue
            
            dep=split[0]
            code=split[1]
            priority=int(split[2])
            course={"dep":dep,
                    "code":code,
                    "priority":priority}
            self.courses.append(course)
    
    def get_sorted_courses(self):
        highest_score=max([c["score"] for c in self.courses])
        
        sorted=[]
        for score in range(highest_score+1):
            for course in self.courses:
                if course["score"]==score:
                    sorted.append(course)
        
        sorted.reverse()
        return sorted
    
    def show(self,show_all=0):
        print("")
        last_status=-1
        sorted_courses=self.get_sorted_courses()
        for course in sorted_courses:
            if show_all or course["score"]:
                self.show_course(course)
    
    def show_course(self,course):
        depcode="%s %s"%(course["dep"],course["code"])
        title=self.cm.get_title_from_depcode(depcode)
        msg1=depcode+" "+title
        msg2=STATUSES[course["status"]]
        
        print(msg1+" "*(50-len(msg1))+" "+msg2)
    
    def set_scores(self):
        highest_priority=0
        for course in self.courses:
            if course["priority"]>highest_priority:
                highest_priority=course["priority"]
        
        for course in self.courses:
            score=highest_priority-course["priority"]+1
            depcode="%s%s"%(course["dep"],course["code"])
            best_crn,best_status=self.cm.get_register_status_by_depcode(depcode)
            
            bad=(NOTACTIVE,NOTFOUND,UNKNOWN)
            if best_status in bad:
                score=0
            
            if best_status==OPEN:
                score+=3
            
            if best_status==WAITLISTOPEN:
                score+=2
            
            course["score"]=score
            course["status"]=best_status
                    
                









