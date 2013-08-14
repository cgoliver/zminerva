import logging, shutil
from string import ascii_lowercase
from os import listdir
from os.path import isdir

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ztools.webpage import WebPage
from course_manager import CourseManager       

class MinervaBot():
    def __init__(self,username,password,headless=0,graduate=0):
        self.username=username
        self.password=password
        self.graduate=graduate
        self.semester=""
        self.course_managers={}
        self.logger=logging.getLogger("mcrawl")
        
        self.display=0
        if headless:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()
        
        self.logger.info("Launching Firefox.")
        self.driver = webdriver.Firefox()
        
        self.login()
        
    def login(self):
        self.logger.info("Logging into Minerva.")
        url="https://horizon.mcgill.ca/pban1/twbkwbis.P_WWWLogin"
        self.driver.get(url)
        
        element = self.driver.find_element_by_id("mcg_un")
        element.send_keys(self.username)
        
        element = self.driver.find_element_by_id("mcg_pw")
        element.send_keys(self.password)
        element.send_keys(Keys.RETURN)
        
        self.logger.debug("Logged into Minerva.")
    
    def set_semester(self,semester):
        "Search class schedule"
        if self.semester==semester:
            return
        else:
            self.semester=semester
            
        url="https://horizon.mcgill.ca/pban1/bwskfcls.p_sel_crse_search"
        self.driver.get(url)
        
        "Combo box for semester"
        found_semester=0
        element = self.driver.find_element_by_id("term_input_id")
        for list_item in element.find_elements_by_tag_name("option"):
            if list_item.text.lower()==semester:
                list_item.click()
                found_semester=1
                break
        if not found_semester:
            self.logger.error("Failed to find semester: %s"%semester)
            return 0
        
        xpath="/html/body/div[3]/form/input[3]"
        submit_button = self.driver.find_element_by_xpath(xpath)
        submit_button.click()
        return 1
    
    def get_course_manager(self,semester,departments):
        if not self.set_semester(semester):
            return 0
        self.submit_course_search(departments)
        
        htmlpath="temp.html"
        with open(htmlpath,"w") as f:
            f.write(self.driver.page_source)
        webpage=WebPage(htmlpath,delete_html=1,verbose=1)
        cm=CourseManager(webpage)
        return cm
    
    def submit_course_search(self,departments):
        dep_text=", ".join(departments).upper()
        self.logger.info("Filling out search for %s classes in departments: %s"%(self.semester,dep_text))
        
        departments=set([d.lower() for d in departments])
                
        "Subject list"
        subject_list = self.driver.find_element_by_id("subj_id")
        
        matchcount=0
        for list_item in subject_list.find_elements_by_tag_name("option"):
            for department in departments:
                if not list_item.text.lower().find(department):
                    matchcount+=1
                    list_item.click()
                    continue
            if matchcount>=len(departments):
                break
        
        if not self.graduate:
            level_list = self.driver.find_element_by_id("levl_id")
            for list_item in level_list.find_elements_by_tag_name("option"):
                if "Undergraduate" in list_item.text:
                    list_item.click()
        
        xpath="/html/body/div[3]/form/input[12]"
        submit_button = self.driver.find_element_by_xpath(xpath)
        submit_button.click()
        
        self.logger.info("Submitting search.")
    
    def close(self):
        self.logger.info("Closing Firefox.")
        self.driver.close()
        if self.display:
            self.display.stop()
        
        self.clear_temp_files()
    
    def clear_temp_files(self):
        """
        selenium seems to have a bug where if the the python process
        never ends, new selenium webdrivers being started will 
        eventually flood the /tmp/ folder with browser profiles.
        This deletes them.
        """
        
        temp_path="/tmp/"
        count=0
        for name in listdir(temp_path):
            path=temp_path+name
            if isdir(path) and not name.find("tmp"):
                shutil.rmtree(path)
                count+=1
            
        self.logger.info("Deleted %s temp files."%count)
        









