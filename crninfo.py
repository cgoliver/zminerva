
class CRNInfo():
    def __init__(self,info_dic):
        self.add_info(info_dic)
        
        self.department=""
        self.code=""
        self.title=""
        self.days=[]
        self.timestart=0
        self.timeend=0
        self.spots=0
        self.instructor=""
        self.status=""
        self.priority=0
        
        
    def add_info(self,info_dic):
        if "department" in info_dic:
            self.department=info_dic["department"]
        
        if "code" in info_dic:
            self.code=info_dic["code"]
        
        if "crn" in info_dic:
            self.crn=info_dic["crn"]
            
        if "title" in info_dic:
            self.title=info_dic["title"]
        
        if "spots" in info_dic:
            try:
                self.spots=int(info_dic["spots"])
            except:
                self.spots=0
        
        if "instructor" in info_dic:
            self.instructor=info_dic["instructor"]
        
        if "status" in info_dic:
            self.status=info_dic["status"]
        
        if "department" in info_dic:
            self.department=info_dic["department"]
        
        if "csv priority" in info_dic:
            self.csvpriority=info_dic["csv priority"]
        
        "days"
        "time"

    def get_priority(self):
        i=0
        try:
            i=int(self.csvpriority)
        except:
            pass
        
        return 10-i*2



