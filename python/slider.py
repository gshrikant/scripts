#! /usr/bin/env python

import sys
import os
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# Exception classes
class FileTypeError:
    pass

class PathError:
    pass

def get_filename():
    """ Get filename from command line arguments """
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "index.html"
        print "No filename specified: using 'index.html'"
    else:
        if filename[-5:] != ".html":
            raise FileTypeError
    return filename

def get_full_path(filename):
    """ Local paths need to be absolute """
    local_path = os.path.abspath(filename)
    if os.path.exists(local_path):
        return local_path
    else:
        raise PathError

def socket_start():
    pass

def driver(address):
    driver = webdriver.Firefox()
    driver.get(address)
    elem = driver.find_element_by_class_name("controls")
    elem.send_keys(Keys.ARROW_RIGHT)
    driver.implicitly_wait(10)

    elem.send_keys(Keys.ARROW_RIGHT)
    driver.implicitly_wait(10)
    elem.send_keys(Keys.ARROW_RIGHT)

    driver.implicitly_wait(10)
    elem.send_keys(Keys.ARROW_RIGHT)

    driver.implicitly_wait(1)
    elem.send_keys(Keys.ARROW_RIGHT)

    driver.implicitly_wait(1)
    elem.send_keys(Keys.ARROW_RIGHT)
    driver.close()

def main():
    try:
        filename = get_filename()
    except FileTypeError:
        print "File type incorrect!"
    else:
        header = 'file:'
        separator = '//'
        try:
            file_path = get_full_path(filename)
        except PathError:
            print "File not found! Check if path is correct and file exists"
        else:
            path = [header, file_path]
            address = separator.join(path)
            print address
            driver(address)

if __name__ == '__main__':
    main()
