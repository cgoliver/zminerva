
import logging, urllib.parse
import subprocess
import requests

from ztools.webpage import WebPage
from course_manager import CourseManager       

class MinervaBot():
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.logger=logging.getLogger("mcrawl")
        self.sessionid=""
        
    def get_sessionid(self):
        if self.sessionid:
            return self.sessionid
        
        url="https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin"
        
        params=(("sid",self.username),
                ("PIN",self.password))
        data=urllib.parse.urlencode(params)
        cookies={"TESTID":"set"}
        
        self.logger.debug("Attempting to login to Minerva.")
        r=requests.post(url,data=data,cookies=cookies)
        self.sessionid=r.cookies.get("SESSID")
        self.logger.info("Logged in to Minerva.")
        
        return self.sessionid
    
    def get_course_page(self,semester,departments):
        url="https://horizon.mcgill.ca/pban1/bwskfcls.P_GetCrse"
        departments=set([d.upper() for d in departments])
        
        data=self.get_data_for_search(semester,departments)
        cookies={"SESSID":self.get_sessionid()}
        
        dep_text=", ".join(departments).upper()
        self.logger.info("Submitting search for %s classes in departments: %s"%(semester,dep_text))
        
        self.logger.debug("cookies: "+str(cookies))
        r=requests.post(url,data=data,cookies=cookies)
        
        return r.text
    
    def get_data_for_search(self,semester,departments):
        start=[("term_in", self.get_term_in(semester)),
                ("sel_subj", "dummy"),
                ("sel_day", "dummy"),
                ("sel_schd", "dummy"),
                ("sel_insm", "dummy"),
                ("sel_camp", "dummy"),
                ("sel_levl", "dummy"),
                ("sel_sess", "dummy"),
                ("sel_instr", "dummy"),
                ("sel_ptrm", "dummy"),
                ("sel_attr", "dummy")]
        
        subjects=[("sel_subj",dep.upper()) for dep in departments]
        
        end=[("sel_crse", ""),
             ("sel_title", ""),
             ("sel_schd", "%"),
             ("sel_from_cred", ""),
             ("sel_to_cred", ""),
             ("sel_levl", "%"),
             ("sel_ptrm", "%"),
             ("sel_instr", "%"),
             ("sel_attr", "%"),
             ("begin_hh", "0"),
             ("begin_mi", "0"),
             ("begin_ap", "a"),
             ("end_hh", "0"),
             ("end_mi", "0"),
             ("end_ap", "a")]
        
        data=urllib.parse.urlencode(start+subjects+end)
        return data
    
    def get_course_manager(self,semester,departments,show_html=0):
        htmldata=self.get_course_page(semester,departments)
        
        if show_html:
            self.show_html(htmldata)
        
        htmlpath="temp.html"
        with open(htmlpath,"w") as f:
            f.write(htmldata)
        webpage=WebPage(htmlpath,delete_html=1,verbose=1)
        cm=CourseManager(webpage)
        return cm
    
    def get_term_in(self,semester):
        seasons={"winter":"01","fall":"09","summer":"05"}
        
        split=semester.split(" ")
        for item in split:
            if item.isdigit():
                year=item
                break
        
        for season in seasons:
            if season in semester:
                month=seasons[season]
                break
        
        try:
            return year+month
        except:
            self.logger.error("Unable to parse semester: %s"%semester)
            return ""
    
    def show_html(self,htmldata):
        htmldata=mb.get_course_page("fall 2013",departments)
        print(htmldata)
        with open("test.html","w") as f:
            f.write(htmldata)
            
        cmd = "chromium-browser test.html"
        status, output = subprocess.getstatusoutput(cmd)















