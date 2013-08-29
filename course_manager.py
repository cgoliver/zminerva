"register status constants"
from zconstants import *

class CourseView():
    def get_row_text(self,row_data):
        r=row_data
        text="\n%s %s - %s"%(r["dep"],r["code"],r["title"])
        for key in self.get_funcs:
            if key not in ("dep","code","title"):
                text+="\n"+"%s: %s"%(key,r[key])
        return text
    
    def get_register_status_by_crn(self,crn):
        if crn not in self.crns:
            if self.logger:
                self.logger.debug("Could not find crn: %s"%crn)
            return NOTFOUND
        
        r=self.crns[crn]
        if r["status"]!="Active":
            return NOTACTIVE
        
        if r["wait act"]==r["wait cap"] and r["wait cap"]>0:
            return WAITLISTFULL
        
        if r["wait act"]<r["wait cap"] and r["wait act"]>0:
            return WAITLISTOPEN
        
        if r["act"] and r["act"]>r["cap"]:
            return OVERBOOKED
        
        if r["rem"]>0:
            return OPEN
        
        return UNKNOWN
    
    def get_register_status_by_depcode(self,depcode):
        depcode=depcode.replace(" ","").upper()
        
        if depcode not in self.depcodes:
            return 0,NOTFOUND
        
        r_statuses={}
        for row_data in self.depcodes[depcode]:
            crn=row_data["crn"]
            rstatus=self.get_register_status_by_crn(crn)
            r_statuses[rstatus]=crn
            
        best_rstatus=list(r_statuses.keys())
        best_rstatus.sort()
        best_status=best_rstatus[-1]
        best_crn=r_statuses[best_status]
        return best_crn,best_status


class CourseManager(CourseView):    
    def __init__(self,webpage,logger=0):
        self.logger=logger
        self.row_datas=[]
        self.depcodes={}
        self.crns={}
        
        self.get_funcs={"crn":self.get_crn,
                        "dep":self.get_dep,
                        "code":self.get_code,
                        "title":self.get_title,
                        "days":self.get_days,
                        "time":self.get_time,
                        "cap":self.get_cap,
                        "act":self.get_act,
                        "rem":self.get_rem,
                        "wait cap":self.get_wait_cap,
                        "wait act":self.get_wait_act,
                        "wait rem":self.get_wait_rem,
                        "prof":self.get_prof,
                        "status":self.get_status}
        
        self.set_webpage(webpage)
    
    def set_webpage(self,webpage):
        self.webpage=webpage
        xpath="/html/body/div[3]/form/table/tr"
        
        for row in webpage.get_from_xpath(xpath):
            self.add_row_element(row)
    
    def get(self,key):
        if key not in self.get_funcs:
            return 0
        
        try:
            value=self.get_funcs[key]()
            if not value:
                return 0
            return value
        except:
            return 0
    
    def get_crn(self):
        return int(self.row[1][0].text)
    def get_dep(self):
        return self.row[2].text
    def get_code(self):
        return self.row[3].text.upper()
    def get_title(self):
        return self.row[7].text
    def get_days(self):
        return self.row[8].text
    def get_time(self):
        return self.row[9].text
    def get_cap(self):
        return int(self.row[10].text)
    def get_act(self):
        return int(self.row[11].text)
    def get_rem(self):
        return int(self.row[12].text)
    def get_wait_cap(self):
        return int(self.row[13].text)
    def get_wait_act(self):
        return int(self.row[14].text)
    def get_wait_rem(self):
        return int(self.row[15].text)
    def get_prof(self):
        return self.row[16].text
    def get_status(self):
        return self.row[19].text
    
    def is_crn(self,value):
        try:
            int(value)
            if value:
                return 1
        except:
            pass
        return 0
    
    def get_depcode(self,row_data):
        return "%s%s"%(row_data["dep"].upper(),row_data["code"])
    
    def add_row_element(self,row):
        self.row=row
        
        row_data={key:self.get(key) for key in self.get_funcs}
        if self.is_crn(row_data["crn"]):
            self.add_row_data(row_data)
    
    def add_row_data(self,row_data):
        if self.logger:
            self.logger.debug(self.get_row_text(row_data))
            
        self.row_datas+=[row_data]
        
        self.crns[row_data["crn"]]=row_data
        
        depcode=self.get_depcode(row_data)
        if depcode not in self.depcodes:
            self.depcodes[depcode]=[]
        self.depcodes[depcode]+=[row_data]

if __name__=="__main__":
    from ztools.webpage import WebPage
    htmlpath="temp.html"
    w=WebPage(htmlpath,verbose=1)
    cm=CourseManager(w,verbose=1)
    print(cm.get_register_status_by_depcode("comp250"))










