#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pywin32
# http://sourceforge.net/projects/pywin32/

# ref
# http://mail.python.org/pipermail/python-win32/2005-March/003077.html

import win32api
import win32gui
import win32con
import getopt
import sys
import re

def FindWindowRegExp(pat):
    p = re.compile(pat)
    # http://www.brunningonline.net/simon/blog/archives/000652.html
    def windowEnumerationHandler(hwnd, resultList):
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

    topWindows = []
    win32gui.EnumWindows(windowEnumerationHandler, topWindows)

    for item in topWindows:
        if p.match(item[1]):
            return item[0]

# http://stackoverflow.com/questions/5080777/what-sendmessage-to-use-to-send-keys-directly-to-another-window
def send_input_hax(hwnd, msg):
    for c in msg:
        if c == "\n":
            win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(c), 0)

def usage():
    print 'usage: sendmsg <window title> <key strokes>'

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError:
        # ヘルプメッセージを出力して終了
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
    
    if len(args) < 2:
        usage()
        sys.exit(2)

    pat = args[0]
    strokes = args[1].replace(r'\n', '\n')

    # find window by regexp
    hwnd = FindWindowRegExp(pat)

    if not hwnd:
    	print 'Window not found'
        sys.exit(1)

    send_input_hax(hwnd, strokes)
    print 'sent message ' + strokes + ' to ' + str(hwnd)

if __name__ == "__main__":
    main()
