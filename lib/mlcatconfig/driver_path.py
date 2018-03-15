import configparser
import os

# mailbox_list = ['lkml', 'opensuse-kernel', 'opensuse-features', 'opensuse', 'opensuse-bugs', 'opensuse-factory', 'sakai-devel']
class Config(configparser.ConfigParser):
    def __init__(self,mailbox):  
        self.cfgfile = os.path.abspath("mlcat.cfg")
        super(Config,self).__init__(allow_no_value=True)
        if os.path.exists(self.cfgfile):
            self.read(self.cfgfile)
       	     
        self.mailbox=mailbox
        
        
    def createVariables(self):
        self.foldername=self.get('param_paths','foldername')+self.mailbox
        self.mbox_filename = self.get('param_paths','foldername') + self.mailbox + '/mbox/' + self.mailbox + '.mbox'
        self.clean_headers_filename = self.get('param_paths','foldername') +self.mailbox + self.get('param_paths','clean_headers_path')
        self.headers_filename = self.get('param_paths','foldername') + self.mailbox +self.get('param_paths','headers_path')
        self.nodelist_filename = self.get('param_paths','foldername') + self.mailbox  +self.get('param_paths','nodelist_path')
        self.edgelist_filename = self.get('param_paths','foldername') + self.mailbox +self.get('param_paths','edgelist_path')
        self.thread_uid_filename =self.get('param_paths','foldername')+ self.mailbox +self.get('param_paths','thread_uid_path')
        self.author_uid_filename = self.get('param_paths','foldername')+ self.mailbox +self.get('param_paths','author_uid_path') 

