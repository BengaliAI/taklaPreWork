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
from .utils import UTILS
#---------------------------------------------------------------
def get_post_time(post_iden):
        '''
            Gets the time string of the post
        '''
        if check(post_iden,XPATHS.CONTENT.TOP):
            top_element=post_iden.find_element_by_xpath(XPATHS.CONTENT.TOP)
            # get time 
            if check(top_element,XPATHS.CONTENT.TIME_STAMP):
                time_element=top_element.find_element_by_xpath(XPATHS.CONTENT.TIME_STAMP)
                string_time=time_element.text
                return string_time
            elif check(top_element,XPATHS.CONTENT.TIME_STAMP_SPAN):
                # get time element
                time_element=top_element.find_element_by_xpath(XPATHS.CONTENT.TIME_STAMP_SPAN)
                string_time=time_element.text
                return string_time    
            else:
                return None

def get_post_author(post_iden):  
    if check(post_iden,XPATHS.CONTENT.TOP):
        top_element=post_iden.find_element_by_xpath(XPATHS.CONTENT.TOP)
        if check(top_element,XPATHS.CONTENT.INFO):    
            # get top info
            info_element=top_element.find_element_by_xpath(XPATHS.CONTENT.INFO)
            # get author and tags/entities
            try:
                auth=info_element.find_element_by_xpath('.//span/h2/strong')
            except NoSuchElementException:
                auth=info_element.find_element_by_xpath('.//span/h2/div/a/strong')
            # author 
            author=auth.text
            return author 
        else:
            return None
    else:
        return None

def get_post_text(post_iden):
    post_text=''
    # check media
    if check(post_iden,XPATHS.CONTENT.MEDIA):
        # get media section
        media_section=post_iden.find_element_by_xpath(XPATHS.CONTENT.MEDIA)
        # image check
        if check(media_section,XPATHS.CONTENT.IMG):
            img=media_section.find_element_by_xpath(XPATHS.CONTENT.IMG)
            # update data
            post_text+=img.get_attribute('alt')
            
    # text
    if check(post_iden,XPATHS.CONTENT.IMAGE_TEXT):
        text_element=post_iden.find_element_by_xpath(XPATHS.CONTENT.IMAGE_TEXT)
        post_text+=text_element.text
    elif check(post_iden,XPATHS.CONTENT.TEXT):
        post_text=''
        text_elements=post_iden.find_elements_by_xpath(XPATHS.CONTENT.TEXT)
        for text_element in text_elements:
            post_text+= text_element.text+"\n"
    elif check(post_iden,XPATHS.CONTENT.TEXT_ALT):
        text_element=post_iden.find_element_by_xpath(XPATHS.CONTENT.TEXT_ALT)
        post_text+=text_element.text

    if post_text.strip():    
        return post_text
    else:
        return None
    

def process_content(post_index,post_iden,container):
    # fill container
    container['id']         =   post_index
    # time
    container['time']       =   UTILS.stringTime(get_post_time(post_iden)).strftime("%d/%m/%Y")
    # get author
    container['author']     =   get_post_author(post_iden)
    # get text 
    container['text']       =   get_post_text(post_iden) 
    # additional
    container['type']       =   'post'
    return container
    
    
    
    
    
    