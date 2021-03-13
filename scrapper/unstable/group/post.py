#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
# ---------------------------------------------------------
from tqdm import tqdm
import json

# ---------------------------------------------------------
# imports
# ---------------------------------------------------------
from .core import *
from .content import *
from .response import *
from .constants import XPATHS
#---------------------------------------------------------------
    
def process_posts(driver,num_posts,json_file):
    post_data=[]
    posts=driver.find_elements_by_xpath(XPATHS.DIVS.POST)
    post_index=0
    for post_iden in tqdm(posts[:num_posts]):
        post_index+=1
        container={}
        # content data
        post_data.append(process_content(post_index,post_iden,container))
        # response data
        post_data=process_comment_section(post_index,post_iden,post_data)
        
    # close
    driver.close()
    print('Closed Driver')
    with open(json_file, "w",encoding='utf8') as write_file:
        json.dump({'data':post_data}, write_file, indent=4,ensure_ascii=False)
    print('Saved Json')