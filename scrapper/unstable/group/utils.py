#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
from datetime import datetime
from dateutil.relativedelta import relativedelta
# ---------------------------------------------------------
import re
# ---------------------------------------------------------

from termcolor import colored

import os 
# -----------------------------------------------------------------------------
def create_folder(folder):
    '''
    checks if specified  folder path exists or not,if no then creates the folder in specified path
    args : 
       folder = contains path as string
    '''
    if not os.path.exists(folder):
        os.mkdir(folder)
# -----------------------------------------------------------------------------

class UTILS:
    @staticmethod
    def ToNumber(string_value):
        '''
            takes string_value and turns it to a number
        '''
        value=None
        # check type
        if not isinstance(string_value, str):
            raise ValueError('Inappropriate type: {}' .format(type(string_value)))
        
        # thousand in terms of K
        if 'K' in string_value:
            
            try:
                value=float(re.findall("[-+]?\d*\.\d+|\d+",string_value)[0])
                value=int(value*1000)
            
            except Exception as e:
                value=0
        
        # any ints
        else:
            try:
                value=int(string_value)
            
            except Exception as e:
                try:
                    value=int(''.join(list(filter(str.isdigit, string_value))))
                
                except Exception as e:
                    value=0
        
        return value

    @staticmethod
    def stringTime(string_time):
        '''
            converts string time to time
        '''
        MONTH_NAMES=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        # cases
        try:
            # get rid of Added
            if 'Added ' in string_time:
                string_time=string_time.replace('Added ','')
            # get rid of Weekday
            if ',' in string_time:
                string_time=string_time.split(',')[1][1:]
            # check if year is in string
            year_check=re.search(r'[12]\d{3}',string_time)
            # named day
            today = datetime.today()
            yesterday= today - relativedelta(days=1)    
            # checks
            if year_check is None:
                if 'at' in string_time:
                    if "Today" in string_time:
                        try:
                            time_obj=datetime.strptime(string_time,'Today at %H:%M')
                        except Exception as e:
                            time_obj=datetime.strptime(string_time,'Today at %I:%M %p')

                        time_obj=time_obj.replace(month=today.month,day=today.day,year=today.year)
                    
                    elif "Yesterday" in string_time:
                        try:
                            time_obj=datetime.strptime(string_time,'Yesterday at %H:%M')
                        except Exception as e:
                            time_obj=datetime.strptime(string_time,'Yesterday at %I:%M %p')

                        time_obj=time_obj.replace(month=yesterday.month,day=yesterday.day,year=yesterday.year)

                    else:
                        try:    
                            time_obj=datetime.strptime(string_time,'%d %B at %H:%M')
                        except Exception as e:
                            time_obj=datetime.strptime(string_time,'%B %d at %I:%M %p')
                        time_obj=time_obj.replace(year=today.year)
                elif any(_month in string_time for _month in MONTH_NAMES) :
                    try:
                        time_obj=datetime.strptime(string_time,'%d %B')
                    except Exception as e:
                        time_obj=datetime.strptime(string_time,'%B %d')

                    time_obj=time_obj.replace(year=today.year)
                else:
                    time_obj=today

            else:
                if 'at' in string_time:
                    try:
                        time_obj=datetime.strptime(string_time,'%d %B %Y at %H:%M')
                    except Exception as e:
                        time_obj=datetime.strptime(string_time,'%B %d %Y at %I:%M %p')

                else:
                    try:
                        time_obj=datetime.strptime(string_time,'%d %B %Y')
                    except Exception as e:
                        time_obj=datetime.strptime(string_time,'%B %d %Y')

            return time_obj

        except Exception as e:
            print(f'Error in time string: {e}')

    @staticmethod
    def ProfileLink(link_string):
        '''
            creates a clean link
        '''
        if "profile.php?id=" in link_string:
            link_string=link_string.split('&')[0]
            link_string=link_string.replace("profile.php?id=",'')
        else:
            link_string=link_string.split('?')[0]

        '''
            group filter
        '''
        if 'groups' in link_string:
            link_string=link_string[:-1]
            link_string="https://www.facebook.com/"+link_string.split('/')[-1] 

        return link_string    
    
    @staticmethod
    def ShortLink(link_string):
        '''
            creates a clean link
        '''

        if "permalink.php?" in link_string:
            link_string=link_string.split('&__cft__[0]')[0]
        else:
            link_string=link_string.split('?__cft__[0]')[0]
            
        return link_string    
    

    
  
    