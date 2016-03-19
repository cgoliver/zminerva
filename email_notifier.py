import smtplib, sys, logging

class EmailNotifier():
    def __init__(self,login,password,
                 logger=0,no_respond_msg=1):
        self.login=login
        self.password=password
        self.logger=logger
        self.no_respond_msg=no_respond_msg
    
    def send_mail(self,email_recipient,subject,body):
        msg=self._get_msg(email_recipient,subject,body)    
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        if self.logger.isEnabledFor(logging.DEBUG):
            self.server.set_debuglevel(1)
        
        result=self._try_login() and self._try_sendmail(msg,email_recipient)                   
        self.server.quit()
        return result
    
    def _try_login(self):
        try:
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.login, self.password)
            return 1
        except:
            self.logger.error("Login for %s failed: %s"%(self.login,sys.exc_info()[0]))
        return 0
    
    def _try_sendmail(self,msg,email_recipient):
        try:
            self.server.sendmail(self.login, email_recipient, msg)
            return 1
        except:
            self.logger.error("Sendmail failed: %s"%sys.exc_info()[0])
        return 0
    
    def _get_msg(self,email_recipient,subject,body):
        msg = ("From: %s\nTo: %s\nSubject: %s\n\n%s"
               % (self.login,email_recipient, subject,body))
        
        if self.no_respond_msg:
            msg+="\n\n-\nThis email was sent from a robot. Reply only if you like talking to robots that never check their mail."
        
        return msg

