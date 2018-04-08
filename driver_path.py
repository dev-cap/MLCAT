import configparser
config = configparser.ConfigParser()
config.read('config.ini')


# mailbox_list = ['lkml', 'opensuse-kernel', 'opensuse-features', 'opensuse', 'opensuse-bugs', 'opensuse-factory', 'sakai-devel']
class driver_path_class:
    def __init__(self,mailbox):        
        self.foldername=config['param_paths']['foldername']+mailbox
        self.mbox_filename = config['param_paths']['foldername'] + mailbox + '/mbox/' + mailbox + '.mbox'
        self.clean_headers_filename = config['param_paths']['foldername'] + mailbox + config['param_paths']['clean_headers_path']
        self.headers_filename = config['param_paths']['foldername'] + mailbox +config['param_paths']['headers_path']
        self.nodelist_filename = config['param_paths']['foldername'] + mailbox  +config['param_paths']['nodelist_path']
        self.edgelist_filename = config['param_paths']['foldername'] + mailbox +config['param_paths']['edgelist_path']
        self.thread_uid_filename = config['param_paths']['foldername']+ mailbox +config['param_paths']['thread_uid_path']
        self.author_uid_filename = config['param_paths']['foldername']+ mailbox +config['param_paths']['author_uid_path']
    	
