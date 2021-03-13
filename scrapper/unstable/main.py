#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
@author: MD.Nazmuddoha Ansary
"""
# ---------------------------------------------------------
from group.scrapper import *
import os
import time
import argparse

# ---------------------------------------------------------
def main(args):
    '''
        scraper wrapper script
    '''
    start_time = time.time()
    save_path=os.path.join(os.getcwd(),'temp')
    url=args.url
    print(url)
    json_path=scrape(url,save_path)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(json_path)

if __name__=='__main__':
    # parsig the arguments from commandline
    parser = argparse.ArgumentParser(description='Group Facebook scraper script',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--url',help="link of the Group to scrape") 
    args = parser.parse_args()
    # execute main
    main(args)
