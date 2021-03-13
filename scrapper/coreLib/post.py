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
from .utils import create_dir,LOG_INFO,UTILS
from .constants import SCRIPTS,XPATHS
from .core import * 

from tqdm import tqdm
import pandas as pd
import numpy as np 
tqdm.pandas()
# -----------------------------------------------------------------------------
# scrapper 
# -----------------------------------------------------------------------------
def get_data(post_url,driver):
    '''
        scrapes a pages data
        
        args:
            post_url    :   url of the post to scrape   
            driver      :   the browser session
        returns:
            _post  and comments  dataframe and the driver session as a tuple            
    '''
    # iterate over 
    URLS=[]
    AUTH=[]
    DATA=[]
    _post={}
    _post['post_url']=[post_url]
    # get url
    try:
        driver.get(post_url)
    except Exception as e:
        print(post_url,e)
        pass
    # wait
    waitSomeTime(2)
    # popup
    if check(driver,XPATHS.POST.NOT_NOW):
        not_now=driver.find_element_by_xpath(XPATHS.POST.NOT_NOW)
        clickLink(not_now)
        waitSomeTime()
    # expand comment section
    if check(driver,XPATHS.POST.DIV):
        post_div=driver.find_element_by_xpath(XPATHS.POST.DIV)
        # post text
        if check(post_div,XPATHS.POST.TEXT):
            _post['text']=[post_div.find_element_by_xpath(XPATHS.POST.TEXT).text]
        else:
            _post['text']=[np.nan]
        # time    
        if check(post_div,XPATHS.POST.TIME):
            _post['time']=[post_div.find_element_by_xpath(XPATHS.POST.TIME).get_attribute("title")]
        else:
            _post['time']=[np.nan]
        # likes
        if check(post_div,XPATHS.POST.LIKES):
            _post['likes']=[UTILS.ToNumber(post_div.find_element_by_xpath(XPATHS.POST.LIKES).text)]
        else:
            _post['likes']=[0]
        
        # shares
        if check(post_div,XPATHS.POST.SHARES):
            _post['shares']=[UTILS.ToNumber(post_div.find_element_by_xpath(XPATHS.POST.SHARES).text)]
        else:
            _post['shares']=[0]
        
        
        # if comment section is not found clink comments
        if not check(post_div,XPATHS.POST.SECTION):
            if check(post_div,XPATHS.POST.COMMENT):
                _link=post_div.find_element_by_xpath(XPATHS.POST.COMMENT)
                _post['comments']=[UTILS.ToNumber(_link.text)]
                clickLink(_link)
                waitSomeTime()
            else:
                _post['comments']=[0]
    # expand comments more
    if check(driver,XPATHS.POST.DIV):
        post_div=driver.find_element_by_xpath(XPATHS.POST.DIV)
        # if comment section is not found clink comments
        if check(post_div,XPATHS.POST.SECTION):
            comment_section=post_div.find_element_by_xpath(XPATHS.POST.SECTION)
            while check(comment_section,XPATHS.POST.MORE):
                _links=comment_section.find_elements_by_xpath(XPATHS.POST.MORE)
                for _link in _links:
                    clickLink(_link)
                    waitSomeTime()
    # check responses
    if check(driver,XPATHS.POST.DIV):
        post_div=driver.find_element_by_xpath(XPATHS.POST.DIV)
        # if comment section is not found clink comments
        if check(post_div,XPATHS.POST.SECTION):
            comment_section=post_div.find_element_by_xpath(XPATHS.POST.SECTION)
            if check(comment_section,XPATHS.POST.RESP):
                responses=comment_section.find_elements_by_xpath(XPATHS.POST.RESP)
                for resp in responses:
                    if check(resp,XPATHS.POST.SEE_MORE):
                        _link=resp.find_element_by_xpath(XPATHS.POST.SEE_MORE)
                        clickLink(_link)
                        waitSomeTime()
                    auth=resp.find_element_by_xpath(XPATHS.POST.AUTH).text
                    data=resp.text.replace(auth,"")
                    URLS.append(post_url)
                    AUTH.append(auth)
                    DATA.append(data)

    _comment=pd.DataFrame({"post":URLS,"author":AUTH,"text":DATA})
    _post=pd.DataFrame(_post)
    return _post,_comment,driver

def post_scrapper(post_urls):
    '''
        urls of the posts to scrape
        args:
            post_urls   :   list of post urls
        returns:
            posts and comments as dataframe
    '''
    posts=[]
    comments=[]
    driver=launchBrowser()
    for post_url in tqdm(post_urls):
        _post,_comment,driver=get_data(post_url,driver)
        posts.append(_post)
        comments.append(_comment)
    posts=pd.concat(posts,ignore_index=False)
    comments=pd.concat(comments,ignore_index=False)
    driver.close()
    return posts,comments