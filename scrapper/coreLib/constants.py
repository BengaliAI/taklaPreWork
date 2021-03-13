#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function

# ---------------------------------------------------------
# class for Scripts
# ---------------------------------------------------------
class SCRIPTS:

    scrollElementIntoMiddle =   "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);"\
                                            + "var elementTop = arguments[0].getBoundingClientRect().top;"\
                                            + "window.scrollBy(0, elementTop-(viewPortHeight/2));"

    scrollHeight            =   "return document.body.scrollHeight"
    
    scroll                  =   "window.scrollTo(0, document.body.scrollHeight);"

    click                   =   "arguments[0].click();"

    scrollDiv               =   "arguments[0].scrollIntoView(false);"
    
    scrollDivShow           =   "arguments[0].scrollIntoView(true);"

# ---------------------------------------------------------
# class for Xpaths
# ---------------------------------------------------------
class XPATHS:
    # xpaths for page data
    class PAGE:
        DIV         =       './/*[@class="_5pcr userContentWrapper"]'
        SECTION     =       './/*[@class="_7a8-"]'
        COMMENT     =       './/a[@class="_3hg- _42ft"]'
        MORE        =       ".//a[@class='_4sxc _42ft']"
        NOT_NOW     =       './/a[@id="expanding_cta_close_button"]'
        RESP        =       ".//*[@class='_72vr']"
        AUTH        =       ".//*[@class='_6qw4']"
        SEE_MORE    =       ".//a[@class='_5v47 fss']"
    # xpaths for post data
    class POST:
        DIV         =       './/*[@class="_5pcr userContentWrapper"]' 
        SECTION     =       './/*[@class="_7a8-"]'
        COMMENT     =       './/a[@class="_3hg- _42ft"]'
        MORE        =       ".//a[@class='_4sxc _42ft']"
        NOT_NOW     =       './/a[@id="expanding_cta_close_button"]'
        RESP        =       ".//*[@class='_72vr']"
        AUTH        =       ".//*[@class='_6qw4']"
        SEE_MORE    =       ".//a[@class='_5v47 fss']"
        TEXT        =       './/*[@data-testid="post_message"]'
        TIME        =       ".//abbr[@class='_5ptz']"
        LIKES       =       ".//*[@class='_81hb']"
        SHARES      =       ".//*[@class='_355t _4vn2']"
        

