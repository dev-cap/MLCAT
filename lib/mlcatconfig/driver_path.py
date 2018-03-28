import configparser
import os

# mailbox_list = ['lkml', 'opensuse-kernel', 'opensuse-features', 'opensuse', 'opensuse-bugs', 'opensuse-factory', 'sakai-devel']
class Config(configparser.ConfigParser):
    def __init__(self,mailbox,cfgfile=None):
        if cfgfile==None:
            cfgfile="mlcat.cfg"
        self.cfgfile=os.path.abspath(cfgfile)
        
        super(Config,self).__init__(allow_no_value=True)
        if os.path.exists(self.cfgfile):
            self.read(self.cfgfile)
       	     
        self.mailbox=mailbox
        
       
    def createVariables(self,section=None):
    	if section==None:
    	    section='param_paths'
    	self.foldername=self.get(section,'foldername')+self.mailbox
    	self.mbox_filename = self.get(section,'foldername') + self.mailbox + '/mbox/' + self.mailbox + '.mbox'
    	self.clean_headers_filename = self.get(section,'foldername') +self.mailbox + self.get(section,'clean_headers_path')
    	self.headers_filename = self.get(section,'foldername') + self.mailbox +self.get(section,'headers_path')
    	self.nodelist_filename = self.get(section,'foldername') + self.mailbox  +self.get(section,'nodelist_path')
    	self.edgelist_filename = self.get(section,'foldername') + self.mailbox +self.get(section,'edgelist_path')
    	self.thread_uid_filename =self.get(section,'foldername')+ self.mailbox +self.get(section,'thread_uid_path')
    	self.author_uid_filename = self.get(section,'foldername')+ self.mailbox +self.get(section,'author_uid_path') 



