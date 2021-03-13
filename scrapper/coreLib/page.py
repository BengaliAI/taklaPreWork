#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
from termcolor import colored
import os 
# -----------------------------------------------------------------------------
# imports
# -----------------------------------------------------------------------------
from .utils import create_dir,LOG_INFO
from .constants import SCRIPTS,XPATHS
from .core import * 

from facebook_scraper import get_posts
from tqdm import tqdm
import pandas as pd
tqdm.pandas()
# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------
DATA_COLS   =       ['post_url','time','text','likes', 'comments','shares']
# -----------------------------------------------------------------------------
# scrapper functions
# -----------------------------------------------------------------------------
def get_post_data(page_id,num_pages=100,save_temp=False):
    '''

        gets only post data i.e: ['post_url','time','text','likes', 'comments','shares']
        args:
            page_id     :       this the page identifier that exists at the end of URL 
                        
                    example:
                        for an url   https://m.facebook.com/MuradTakla page_id="MuradTakla"
            num_pages   :       the number of pages determines the number of posts
                                usually there are 4*num_pages posts  (default:100)
            save_temp   :       save the posts data temporarily , the default folder 
                                to save data is /temp folder        (default:False)
        returns:
            a dataframe with the described columns 
    '''
    # the facebook_scrapper get posts call
    page_data=get_posts(page_id, pages=num_pages)
    # turn data into jsons
    _jsons=[data for data in tqdm(page_data)]
    # json to dataframe
    df=pd.DataFrame(_jsons)
    # select data columns to keep
    df=df[DATA_COLS]
    if save_temp:
        temp_dir        =   create_dir(os.path.join(os.getcwd()),'temp')
        post_csv_path   =   os.path.join(temp_dir,f"{page_id}_{num_pages}_posts.csv")
        df.to_csv(post_csv_path,index=False)
    return df 

def get_comment_data(post_urls):
    '''
        scrapes comments and replies from given URL :  [post_url,author,text]
        args:
            post_urls   :   urls of the posts to be scrapped
        returns:
            a dataframe with the described columns 
    '''
    # launch driver
    driver=launchBrowser()
    # iterate over post urls 
    URLS=[]
    AUTH=[]
    DATA=[]
    for post_url in tqdm(post_urls): 
        
        # get url
        try:
            driver.get(post_url)
        except Exception as e:
            LOG_INFO(f"Problem in getting data from:{post_url}",mcolor="cyan")
            LOG_INFO(f"error:{e}",mcolor="red")
            pass
        
        # wait
        waitSomeTime(2)
        # pop up
        if check(driver,XPATHS.PAGE.NOT_NOW):
            not_now=driver.find_element_by_xpath(XPATHS.PAGE.NOT_NOW)
            clickLink(not_now)
            waitSomeTime()
        # expand comment section
        if check(driver,XPATHS.PAGE.DIV):
            post_div=driver.find_element_by_xpath(XPATHS.PAGE.DIV)
            # if comment section is not found clink comments
            if not check(post_div,XPATHS.PAGE.SECTION):
                if check(post_div,XPATHS.PAGE.COMMENT):
                    _link=post_div.find_element_by_xpath(XPATHS.PAGE.COMMENT)
                    clickLink(_link)
                    waitSomeTime()

        # expand comments more
        if check(driver,XPATHS.PAGE.DIV):
            post_div=driver.find_element_by_xpath(XPATHS.PAGE.DIV)
            # if comment section is not found clink comments
            if check(post_div,XPATHS.PAGE.SECTION):
                comment_section=post_div.find_element_by_xpath(XPATHS.PAGE.SECTION)
                while check(comment_section,XPATHS.PAGE.MORE):
                    _links=comment_section.find_elements_by_xpath(XPATHS.PAGE.MORE)
                    for _link in _links:
                        clickLink(_link)
                        waitSomeTime()
        # check responses
        if check(driver,XPATHS.PAGE.DIV):
            post_div=driver.find_element_by_xpath(XPATHS.PAGE.DIV)
            # if comment section is not found clink comments
            if check(post_div,XPATHS.PAGE.SECTION):
                comment_section=post_div.find_element_by_xpath(XPATHS.PAGE.SECTION)
                if check(comment_section,XPATHS.PAGE.RESP):
                    responses=comment_section.find_elements_by_xpath(XPATHS.PAGE.RESP)
                    for resp in responses:
                        if check(resp,XPATHS.PAGE.SEE_MORE):
                            _link=resp.find_element_by_xpath(XPATHS.PAGE.SEE_MORE)
                            clickLink(_link)
                            waitSomeTime()
                        auth=resp.find_element_by_xpath(XPATHS.PAGE.AUTH).text
                        data=resp.text.replace(auth,"")
                        URLS.append(post_url)
                        AUTH.append(auth)
                        DATA.append(data)
    # dataframe                    
    df=pd.DataFrame({"post_url":URLS,"author":AUTH,"text":DATA})
    driver.close()
    return df

    
# -----------------------------------------------------------------------------
# scrapper 
# -----------------------------------------------------------------------------
def page_scrapper(page_ids,num_pages=100):
    '''
        scrapes a pages data
        
        args:
            page_ids    :   ids of pages to scrape
            num_pages   :   the number of pages determines the number of posts
                            usually there are 4*num_pages posts  (default:100)
        returns:
            posts and comments dataframe as a tuple            
    '''
    posts=[]
    LOG_INFO("Getting Post Data")
    for page_id in tqdm(page_ids):
        posts.append(get_post_data(page_id,num_pages=num_pages))
    posts=pd.concat(posts,ignore_index=True)
    
    LOG_INFO("Getting Comment Data")
    post_urls=posts.post_url.tolist()
    comments=get_comment_data(post_urls)

    return posts,comments