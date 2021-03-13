#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
# ---------------------------------------------------------
# class for xpaths
# ---------------------------------------------------------
class XPATHS:
    # for getting links
    LINK                =       ".//a[@role='link']"         
    class BUTTONS:
        # comments
        MORE_COMMENTS       =       ".//span[text()[contains(.,'more comments') or contains(.,'View previous comments') or contains(.,'more comment')]]"
        # replies
        MORE_REPLIES        =       ".//span[@class='j83agx80 fv0vnmcu hpfvmrgz']"
        # see more 
        SEE_MORE            =       ".//div[text()[contains(.,'See more')]]"
        # ok button
        OK                  =       ".//*[@aria-label='OK']"
        # close chat
        CHAT                =       ".//div[@aria-label='Close chat']"
        
    class DIVS:
        # POST
        POST                =       ".//div[@class='du4w35lb l9j0dhe7']"
        # engagement (share,comments)
        ENGAZEMENT          =       ".//div[@class='bp9cbjyn m9osqain j83agx80 jq4qci2q bkfpd7mw a3bd9o3v kvgmc6g5 wkznzc2l oygrvhab dhix69tm jktsbyx5 rz4wbd8a osnr6wyh a8nywdso s1tcr66n']"         
        ENGAZEMENT_ACTS     =       ".//div[@class='gtad4xkn']"
        # the whole comment section
        COMMENT_SECTION     =       ".//div[@class='cwj9ozl2 tvmbv18p']"
    class CONTENT:
        # gets post top that contains author,time and post information
        TOP                 =       ".//div[@class='pybr56ya dati1w0a hv4rvrfc n851cfcs btwxx1t3 j83agx80 ll8tlv6m']"
        ## time stamp with link
        TIME_STAMP          =       ".//*[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']"
        ## just the text
        TIME_STAMP_SPAN     =       ".//span[@class='tojvnm2t a6sixzi8 abs2jz4q a8s20v7p t1p8iaqh k5wvi7nf q3lfd5jv pk4s997a bipmatt0 cebpdrjk qowsmv63 owwhemhu dp1hu0rb dhp61c6y iyyx5f41']"
        # top post info
        INFO                =       ".//div[@class='qzhwtbm6 knvmm38d']"          
        # gets the post text
        TEXT                =       ".//div[@data-ad-preview='message']"
        TEXT_ALT            =       ".//div[@class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']"
        IMAGE_TEXT          =       ".//div[@class='k4urcfbm']"
        # announcement
        EXCLUDE             =       ".//div[@class='btwxx1t3 j83agx80']"
        # media data
        MEDIA               =       ".//div[@class='l9j0dhe7']"
        IMG                 =       ".//img[@class='i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm bixrwtb6']"
        
    class RESPONSE:
        AUTHOR              =       ".//*[@class='nc684nl6']"
        TEXT                =       ".//*[@class='ecm0bbzt e5nlhep0 a8c37x1j']"
        TIME                =       ".//*[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl m9osqain gpro0wi8 knj5qynh']"
        # media data
        IMAGE               =       ".//img[@class='img]"
    

       


    

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

