#! /usr/bin/env python

# Simple script to download the top wallpaper from /r/Wallpapers subreddit
# Author: Shrikant Giridhar
# Date: September 4, 2014
# License: MIT

import urllib
import re
import os
from random import randrange
from bs4 import BeautifulSoup

def make_dir(tmp):
    """ Create a temporary directory to store files """
    if not os.path.exists("tmp"):
        os.mkdir(tmp)
        os.chdir(tmp)
    else:
    #    print "Path exists! Specify a different directory name"
        os.chdir(tmp)
        

def get_page(pg_link):
    """ Get the HTML source """
    link_list = []
    response = urllib.urlopen(pg_link)
    html = response.read()
    soup = BeautifulSoup(html)
    for link in soup.find_all('a', href=re.compile("jpg|imgur")):
        link_list.append(str(link.get('href')))
    return link_list

def filter_links(link_list, filter_list):
    """ Remove extraneous keywords and image links """
    for pattern in filter_list:
        for link in link_list:
            if re.search(pattern, link):
                link_list.remove(link) 
    link_list = sorted(set(link_list))      # Nice trick to remove duplicate entries
    return link_list

def get_img(img_link, file_path):
    urllib.urlretrieve(img_link, file_path)

def set_wpaper(pic_path):
    cmd_str = "gconftool-2 --set /desktop/gnome/background/picture_filename \
            --type string " + pic_path
    os.system(cmd_str)

##TODO: Append .jpg to all imgur indirect links
##TODO: Add .png support

def main():
    filter_pattern = ["reddit", "domain"]
    make_dir("tmp")
    file_path = os.getcwd() + "/wall.jpg"
    all_links = get_page("http://www.reddit.com/r/wallpapers/top")
    img_links = filter_links(all_links, filter_pattern)
    rand_index = randrange(0, len(img_links))
    get_img(img_links[rand_index], file_path)
    set_wpaper(file_path)
#    print img_links

if __name__ == '__main__':
    main()








