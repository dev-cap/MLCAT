import pytest
import configparser
import os

def test_config_class():
    t_config=Config('t_mailbox')
    t_config.createVariables()

    assert t_config.foldername =='./data/t_mailbox'
    assert t_config.mbox_filename=='./data/t_mailbox/mbox/t_mailbox.mbox'
    assert t_config.clean_headers_path=='./data/t_mailbox/json/clean_data.json'
    assert t_config.nodelist_path =='./data/t_mailbox/tables/graph_nodes.csv'
    assert t_config.edgelist_path =='./data/t_mailbox/tables/graph_edges.csv'
    assert t_config.thread_uid_path =='.data/t_mailbox/json/thread_uid_map.json'
    assert t_config.author_uid_path =='./data/t_mailbox/json/author_uid_map.json'
    assert t_config.headers_path =='./data/t_mailbox/json/headers.json'

