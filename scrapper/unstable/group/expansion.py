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
def expand_comment(post_iden):
    # if there is engagement
    if check(post_iden,XPATHS.DIVS.ENGAZEMENT):
        acts=post_iden.find_elements_by_xpath(XPATHS.DIVS.ENGAZEMENT_ACTS)
        for act in acts:
            # if there is comment
            if "comment" in act.text:
                # if there is no commnent section
                if not check(post_iden,XPATHS.DIVS.COMMENT_SECTION):
                    clickLink(act)
                    waitSomeTime()
            

def expand_section(post_iden):
    if check(post_iden,XPATHS.DIVS.COMMENT_SECTION):
        # more Comments
        while check(post_iden,XPATHS.BUTTONS.MORE_COMMENTS):
            mores=post_iden.find_elements_by_xpath(XPATHS.BUTTONS.MORE_COMMENTS)
            for more in mores:
                clickLink(more)
                waitSomeTime(2)
    
        # more replies
        if check(post_iden,XPATHS.BUTTONS.MORE_REPLIES):
            mores=post_iden.find_elements_by_xpath(XPATHS.BUTTONS.MORE_REPLIES)
            for more in mores:
                if "Hide" not in more.text:
                    clickLink(more)
                    waitSomeTime(2)

        # see mores
        while check(post_iden,XPATHS.BUTTONS.SEE_MORE):
            mores=post_iden.find_elements_by_xpath(XPATHS.BUTTONS.SEE_MORE)
            for more in mores:
                clickLink(more)
                waitSomeTime(2)

    
