
import time
from zconstants import STATUSES
from ztools.email_notifier import EmailNotifier

class LoopMessenger():
    def report(self):
        if not self.can_send_email() or not self.report_days:
            return
        
        time_since_last_report=time.time()-self.last_report_time
        if time_since_last_report<self.report_days*24*60*60:
            return
        
        self.last_report_time=time.time()
        self.send_report_email()
    
    def send_report_email(self):
        messages=[]
        for item in self.last_course_history:
            s_msg=STATUSES[item["status"]]
            msg="%s for %s with CRN %s is \"%s\"."%(item["depcode"].upper(),item["semester"],item["crn"],s_msg)
            messages+=[msg]
        
        subject="zminerva report"
        body="Hello.\n\nHere's the regular status report you requested every %s day(s):\n\n"%self.report_days
        body+="\n".join(messages)
        body+="\n\nzminerva will continue to check class statuses every %s seconds."%self.interval
        
        self.send_email(subject,body)

    def can_send_email(self):
        return self.gmail_user and self.gmail_pw and self.gmail_recipient
    
    def send_update_email(self,changed_items):
        if not self.can_send_email():
            return
        
        messages=[]
        for item in changed_items:
            s_msg=STATUSES[item["status"]]
            msg="%s for %s with CRN %s is now \"%s\"."%(item["depcode"].upper(),item["semester"],item["crn"],s_msg)
            messages+=[msg]
        
        depcodes=[i["depcode"].upper() for i in changed_items]
        subject="Minerva update for %s"%(", ".join(depcodes))
        body="Hello.\n\nSome McGill courses you are monitoring have changed their status:\n%s\n\nTo log in:\nhttps://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin"
        body=body%"\n".join(messages)
        
        self.send_email(subject,body)
    
    def send_email(self,subject,body):
        self.logger.info("Sending email \"%s\" to: %s"%(subject,self.gmail_recipient))
        en=EmailNotifier(self.gmail_user,self.gmail_pw,
                         logger=self.logger)
        en.send_mail(self.gmail_recipient,subject,body)
        









