# -*-coding: utf-8 -
'''
    @author:  MD. Nazmuddoha Ansary
'''
#--------------------
# imports
#--------------------
import os 
import json
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from coreLib.utils import create_dir,LOG_INFO
from coreLib.page import page_scrapper
from coreLib.post import post_scrapper
#--------------------
# main
#--------------------
def main():
    '''
        * scrapes data based on config.json
    '''      
    with open('config.json') as json_file:
        data = json.load(json_file)
    # get config 
    _type       =   data["type"]
    _ids        =   data["ids"]
    _save_path  =   data["save_path"]          
    # select scrapper
    if _type=="page":
        page_ids=_ids
        posts,comments=page_scrapper(page_ids=page_ids)
    if _type=="post":
        post_urls=_ids
        posts,comments=post_scrapper(post_urls)
    # combine data
    posts_data_path   =   os.path.join(os.path.join(_save_path,f'posts_{datetime.now().strftime("%m_%d_%Y_%H_%M")}.csv'))    
    comms_data_path   =   os.path.join(os.path.join(_save_path,f'comments_{datetime.now().strftime("%m_%d_%Y_%H_%M")}.csv'))
    # save data
    posts.to_csv(posts_data_path,index=False)
    comments.to_csv(comms_data_path,index=False)
    
    posts       =   posts[["text"]]
    comments    =   comments[["text"]]
    # create save dir
    data_path   =   os.path.join(os.path.join(_save_path,f'{datetime.now().strftime("%m_%d_%Y_%H_%M")}.csv'))    
    data        =   pd.concat([posts,comments],ignore_index=True)
    data.to_csv(data_path,index=False)
    
#-----------------------------------------------------------------------------------

if __name__=="__main__":
    main()
    
    