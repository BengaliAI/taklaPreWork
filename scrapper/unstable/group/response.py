#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
# ---------------------------------------------------------
# imports
# ---------------------------------------------------------
from .core import *
from .constants import XPATHS
#---------------------------------------------------------------
def get_comment_time(comment):
    if check(comment,XPATHS.RESPONSE.TIME):
        return comment.find_element_by_xpath(XPATHS.RESPONSE.TIME).text
    else:
        return None

def get_comment_text(comment):
    text_data=''
    # image check
    if check(comment,XPATHS.RESPONSE.IMAGE):
        img=comment.find_element_by_xpath(XPATHS.RESPONSE.IMAGE)
        # update data
        text_data+=img.get_attribute('alt')
        
    if check(comment,XPATHS.RESPONSE.TEXT):
        text_data+= comment.find_element_by_xpath(XPATHS.RESPONSE.TEXT).text
    if text_data.strip():
        return text_data
    else:
        return None
    
def get_comment_author(comment):
    if check(comment,XPATHS.RESPONSE.AUTHOR):
        auth=comment.find_elements_by_xpath(XPATHS.RESPONSE.AUTHOR)[1]
        return auth.text
    else:
        return None

def get_comment_type(comment):
    if "Reply" in comment.get_attribute("aria-label"):
        return 'reply'
    else:
        return 'comment'
    

def process_comment(comment,post_index):
    if check(comment,XPATHS.RESPONSE.TEXT):
        container={}
        # fill container
        container['id']         =   post_index
        # time
        container['time']       =   get_comment_time(comment)
        # get author
        container['author']     =   get_comment_author(comment)
        # get text 
        container['text']       =   get_comment_text(comment)
        # additional
        container['type']       =   get_comment_type(comment)
        return container
        
        
    else:
        return None
    

def process_comment_section(post_index,post_iden,post_data):
    if check(post_iden,XPATHS.DIVS.COMMENT_SECTION):
        comment_section=post_iden.find_element_by_xpath(XPATHS.DIVS.COMMENT_SECTION)
        if check(comment_section,'.//div[@role="article"]'):
            comments=comment_section.find_elements_by_xpath('.//div[@role="article"]')
            for comment in comments:
                data=process_comment(comment,post_index)
                if data is not None:
                    post_data.append(data)

            return post_data
            
        else:
            return post_data
    else:
        return post_data
    
    
    
    
    
    
    