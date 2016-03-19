
import re
import requests, charade

from lxml import etree
from io import StringIO

class WebPageView():
    """
    abstract class to be inherited by WebPage.
    """
    def get_from_xpath(self, xpath):
        """
        returns a list of elements that match the xpath.
        
        lxml doesn't seem to like complex xpaths, keep it simple:
        /html/body/div[5]/div/div[2]/div
        """
        if self.tree:
            return self.tree.xpath(xpath)
        return list()
    
    def search_elements(self, query):
        """
        returns a list of elements that contain the string query
        """
        if type(self.root) == int:
            return []
        elements = []
        reg = re.compile("[ ]+")
        for element in self.root.iter():
            text = "" if not element.text else reg.sub(" ", element.text)
            tail = "" if not element.tail else reg.sub(" ", element.tail)
            if ((element.text and query in text) or
                (element.tail and query in tail)) and element.tag != "script":
                elements += [element]
        
        return elements
    
    def show_query(self,query):
        """
        prints information on all elements containing the string
        query
        """
        for element in self.search_elements(query):
            self.show_element(element)
    
    def show_element(self,element):
        print("xpath: %s"%self.tree.getpath(element))
        if element.text and element.text.strip():
            print(element.text.strip())
        if element.tail and element.tail.strip():
            print(element.tail.strip())
    

class WebPage(WebPageView):
    """
    initialize with either a url, a path to an html, or html data.
    WebPage will get the data, guess its encoding, decode it,
    and use lxml to build a lxml tree and lxml root.
    """
    def __init__(self, url="",htmlpath="",htmldata="", 
                 encoding="",verbose=0,delete_html=0):
        self.url=url
        self.htmlpath=htmlpath
        self.htmldata=htmldata
        self.encoding=encoding
        self.verbose = verbose
        
        self._set_htmldata()
        
        self._replace_htmldata_tags()
        self._parse_htmldata()
    
    def write(self,filename):
        with open(filename,"w") as f:
            f.write(self.htmldata)
    
    def _set_htmldata(self):
        if not self.url and not self.htmlpath and not self.htmldata:
            raise TypeError("WebPage requires a url, htmlpath, or htmldata on initialization.")
        
        if self.url:
            if "://" not in self.url:
                self.url="http://"+self.url
            
            self._use_url()
            return
        
        if self.htmlpath:
            self._use_htmlpath()
            return
        
        if self.htmldata:
            if type(self.htmldata) is bytes:
                self._use_htmlbytes(self.htmldata)
            return
    
    def _use_url(self):
        r=requests.get(self.url)
        if not self.encoding:
            self.encoding=r.encoding
        
        self.htmldata=r.text
    
    def _use_htmlpath(self):
        with open(self.htmlpath,"rb") as f:
            htmlbytes=f.read()
        self._use_htmlbytes(htmlbytes)
    
    def _use_htmlbytes(self,htmlbytes):
        encoding=charade.detect(htmlbytes)["encoding"]
        self.htmldata=htmlbytes.decode(encoding=encoding)
    
    def _replace_htmldata_tags(self):
        """
        this is a dirty hack to handle a fishy way that some
        websites use self closing tags.
        """
        self.htmldata = self.htmldata.replace("<br />", "\n")
    
    def _parse_htmldata(self):
        parser = etree.HTMLParser(encoding="utf-8",
                                remove_comments=1)
        
        try:
            self.tree = etree.parse(StringIO(self.htmldata), parser)
            self.root = self.tree.getroot()
            if self.tree.getroot() is None:
                raise IOError()
        except:
            self.root, self.tree = None, None
            if self.verbose:
                print("Failed to parse page: %s"%self.url_or_htmlpath)


    
    
    
    
    
