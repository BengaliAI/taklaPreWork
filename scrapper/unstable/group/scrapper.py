#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
# ---------------------------------------------------------
from tqdm.auto import tqdm
import os 
from datetime import datetime
# ---------------------------------------------------------
# imports
# ---------------------------------------------------------
from .core import *
from .expansion import *
from .post import *
from .constants import XPATHS
from .utils import create_folder
#---------------------------------------------------------------
# global fixed
POSTS_NEEDED=100
#---------------------------------------------------------------


def expand_and_scroll(driver):
    # record valid post elements
    all_posts =[]
    num_posts =0
    scroll_count=0
    post_count=0
    if check(driver,XPATHS.DIVS.POST):
        while num_posts<POSTS_NEEDED:
            # get post elements
            current_posts=driver.find_elements_by_xpath(XPATHS.DIVS.POST)
            # update all elements
            num_posts=len(current_posts)
            # new posts
            new_posts=[post_iden for post_iden in current_posts if post_iden not in all_posts]
            all_posts=current_posts
            for post_iden in tqdm(new_posts):
                if post_count==POSTS_NEEDED:
                    break
                else:
                    expand_comment(post_iden)
                    expand_section(post_iden)
                    post_count+=1
            
            
            if post_count==POSTS_NEEDED:
                # update log
                LOG_INFO=f"POST_COUNT:{num_posts},scroll_count:{scroll_count}"
                print(LOG_INFO)
                
                break
                
            # scroll
            scroll()
            waitSomeTime()
            # update log
            LOG_INFO=f"POST_COUNT:{num_posts},scroll_count:{scroll_count}"
            print(LOG_INFO)
            scroll_count+=1



def scrape(url,save_path):
    '''
        get things started to scrape
    '''
    try:
        # create save path
        create_folder(save_path)
        # process url
        PROCEED=False
        BASE="https://www.facebook.com/groups/"
        if BASE not in url:
            ERROR_LOG="Not in www.facebook.com"
            PROCEED=False
            print(ERROR_LOG)
            exit(1)
        else:
            if "groups" not in url:
                ERROR_LOG="Not a Group"
                PROCEED=False
                print(ERROR_LOG)
                exit(1)
            else:
                ENTITY=url.replace(BASE,'')
                if '/' in ENTITY:
                    ENTITY=ENTITY.split('/')[0]    
                PROCEED=True

        if PROCEED:
            SORTING_EXT="/?sorting_setting=CHRONOLOGICAL"
            URL=BASE+ENTITY+SORTING_EXT
            
            # launch browser
            driver=launchBrowser()
            # load page
            loadPage(URL)
            # driver action
            expand_and_scroll(driver)
            # save
            json_path=os.path.join(save_path,f'{ENTITY}_{str(datetime.now().strftime("%H_%M_%d_%m_%Y"))}.json')
            process_posts(driver,POSTS_NEEDED,json_path)
            return json_path
    
    except Exception as e:
        print(e)
        
    

     
                   
    
