import time, os.path, logging, sys, datetime

from http.client import BadStatusLine
from selenium.common.exceptions import WebDriverException

from minerva_bot import MinervaBot
from ztools.email_notifier import EmailNotifier
from ztools.zio import zread_json, zwrite_json
from zconstants import *

class MinervaLoop():
    def __init__(self,mcgill_user,mcgill_pw,
                 watchlist,
                 interval=300,
                 headless=0,
                 verbose=0,
                 gmail_user="",gmail_pw="",gmail_recipient="",
                 args={}):
        self.mcgill_user=mcgill_user
        self.mcgill_pw=mcgill_pw
        self.headless=headless
        self.gmail_user=gmail_user
        self.gmail_pw=gmail_pw
        self.gmail_recipient=gmail_recipient
        self.watchlist=watchlist
        self.verbose=verbose
        self.args=args
        
        self.logger=logging.getLogger("mcrawl")
        
        self.course_history=[]
        
        self.set_semester_dic()
        self.loop(interval)
    
    def set_semester_dic(self):
        """
        semester_dic keys are semester strings
        
        semester_dic values are sets of all departments that have 
        watched courses that semester
        
        {'winter 2013': {'comp'}, 'fall 2013': {'comp', 'edpe'}}
        """
        watchdic={}
        for item in self.watchlist:
            semester=item["semester"]
            if semester not in watchdic:
                watchdic[semester]=[]
            watchdic[semester]+=[item]
        
        self.semester_dic={}
        for semester in watchdic:
            departments=[i["dep"] for i in watchdic[semester]]
            self.semester_dic[semester]=set(departments)
        
    def loop(self,interval):
        first=1
        failcount=0
        while 1==1:
            self.set_logger()
            if first:
                self.logger.info("Starting Minerva monitoring with args:\n"+str(self.args))
                first=0
                
            success=self.try_run()
            if success:
                failcount=0
            else:
                failcount+=1
                if failcount>30:
                    failcount=30
                
            real_interval=int(interval*(1+failcount/2))
            self.logger.info("Waiting %s seconds."%real_interval)
            time.sleep(interval)
    
    def try_run(self):
        try:
            self.run()
            return 1
        except (BadStatusLine, IOError) as e:
            self.logger.error("Connection failed.",exc_info=1)
        except WebDriverException as e:
            self.logger.critical("Webdriver failed: "+str(e))
        except:
            self.logger.error("Unknown failure.",exc_info=1)
        return 0
    
    def run(self):
        mb=MinervaBot(self.mcgill_user,self.mcgill_pw,
                      headless=self.headless)
        
        try:
            for semester in self.semester_dic:
                departments=self.semester_dic[semester]
                cm=mb.get_course_manager(semester,departments)
                if not cm:
                    self.logger.error("Failed to get course manager for %s %s"%(semester,", ".join(departments)))
                    continue
                
                for watchitem in self.watchlist:
                    if watchitem["semester"]==semester:
                        self.lookup(watchitem,cm)
        
            self.process_course_history()
        finally:
            mb.close()
                    
    
    def lookup(self,watchitem,course_manager):
        crn=watchitem["crn"]
        depcode=watchitem["depcode"]
        if crn:
            status=course_manager.get_register_status_by_crn(crn)
        else:
            crn,status=course_manager.get_register_status_by_depcode(depcode)
        
        item={"crn":crn,"depcode":depcode,
              "status":status,"semester":watchitem["semester"]}
        self.logger.debug("found info: %s %s %s"%(crn,depcode,status))
        self.course_history+=[item]

    def set_logger(self):
        def get_log_name():
            dt=datetime.datetime.now()
            return "%s-%s-%s-mcrawl.log"%(dt.year,dt.month,dt.day)
        
        self.logger = logging.getLogger("mcrawl")
        if self.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
    
        fh = logging.FileHandler("logs/"+get_log_name())    
        ch = logging.StreamHandler()
        
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.handlers=[]
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def log_status_summary(self):
        statuses={}
        for item in self.course_history:
            s=item["status"]
            if s not in statuses:
                statuses[s]=[]
            statuses[s]+=[item]
            
        summary=""
        for s in statuses:
            depcodes=[item["depcode"].upper() for item in statuses[s]]
            summary+="\"%s\": %s. "%(STATUSES[s],", ".join(depcodes))
        self.logger.info(summary)
    
    def process_course_history(self):
        path="course_history"
        self.log_status_summary()
        
        if os.path.isfile(path):
            old_history=zread_json(path)
            if old_history:
                self.compare_history(old_history)
            else:
                self.logger.warning("Failed to find %s."%path)
        
        zwrite_json(self.course_history,path,verbose=0)
        self.course_history=[]
    
    def compare_history(self,old_history):
        def is_match(item1,item2):
            return (item1["depcode"]==item2["depcode"] and
                    item1["crn"]==item2["crn"])
        
        changed_items=[]
        for item1 in old_history:
            for item2 in self.course_history:
                if is_match(item1,item2):
                    if item1["status"]!=item2["status"]:
                        changed_items+=[item2]
        
        if changed_items:
            self.logger.info("Course statuses have changed.")
            self.logger.debug(str(changed_items))
            if self.can_send_email():
                self.send_email(changed_items)
    
    def can_send_email(self):
        return self.gmail_user and self.gmail_pw and self.gmail_recipient
    
    def send_email(self,changed_items):
        messages=[]
        for item in changed_items:
            s_msg=STATUSES[item["status"]]
            msg="%s for %s with CRN %s is now \"%s\"."%(item["depcode"].upper(),item["semester"],item["crn"],s_msg)
            messages+=[msg]
        
        depcodes=[i["depcode"].upper() for i in changed_items]
        subject="Minerva update for %s"%(", ".join(depcodes))
        body="Hello.\n\nSome McGill courses you are monitoring have changed their status:\n%s\n\nTo log in:\nhttps://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin"
        body=body%"\n".join(messages)
        
        self.logger.info("Sending email to: %s"%self.gmail_recipient)
        en=EmailNotifier(self.gmail_user,self.gmail_pw,
                         logger=self.logger)
        en.send_mail(self.gmail_recipient,subject,body)
        
def get_course_string(depcode, semester,crn):
    return 
                
            






