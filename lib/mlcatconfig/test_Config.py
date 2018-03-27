import pytest
import configparser
import os
#from testfixtures import TempDirectory
from driver_path import *



    
def test_config_class():
    
    path=os.path.abspath("mlcat.cfg")
    if ' ' in path:
        assert False
        
    t_config=Config('t_mailbox')
    t_config.read(path)
    t_config.createVariables();
    
    assert t_config.foldername =='./data/t_mailbox'
    assert t_config.mbox_filename=='./data/t_mailbox/mbox/t_mailbox.mbox'
    assert t_config.clean_headers_filename=='./data/t_mailbox/json/clean_data.json'
    assert t_config.nodelist_filename =='./data/t_mailbox/tables/graph_nodes.csv'
    assert t_config.edgelist_filename =='./data/t_mailbox/tables/graph_edges.csv'
    assert t_config.thread_uid_filename =='./data/t_mailbox/json/thread_uid_map.json'
    assert t_config.author_uid_filename =='./data/t_mailbox/json/author_uid_map.json'
    assert t_config.headers_filename =='./data/t_mailbox/json/headers.json'
    
    
@pytest.fixture(scope='session')
def test_diff_dir_config(tmpdir_factory):
    
    p = tmpdir_factory.mkdir("test_dir").join("test_file.cfg")
    cfgfile = open(p, 'w')
    test_cfg = ConfigParser.ConfigParser()
    test_cfg.add_section('path_test')
    test_cfg.set('path_test', 'foldername', './t_data/test_file/')
    test_cfg.write(cfgfile)
    cfgfile.close()
    
    t_config=Config('t_mailbox',p)
    t_config.read(p.path)
    t_config.createVariables('path_test');
    assert t_config.foldername=='./t_data/test_file/t_mailbox'
