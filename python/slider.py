#! /usr/bin/env python
## slider.py
## Control a HTML presentation using browser automation (Selenium)
## Receives control characters over a socket connection
## TODO: custom keybindings from a file

import sys
import os
import socket
import SocketServer
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

class SocketService(SocketServer.BaseRequestHandler):
    def handle(self):
        print self.client_address
        while True:
            self.data = self.request.recv(1024)
            if not self.data:
                break
            self.data = self.data.strip()
            print self.data
            self.server.ctl.send_keys(Keys.ARROW_RIGHT)

        print "Client closed socket"


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def setup_webdriver(address):
    driver = webdriver.Firefox()
    driver.get(address)
    elem = driver.find_element_by_class_name("controls")
    return elem

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
            ctl = setup_webdriver(address)

    t = ThreadedTCPServer(('', 5300), SocketService)
    t.ctl = ctl
    t.serve_forever()

if __name__ == '__main__':
    main()
