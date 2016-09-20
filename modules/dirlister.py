#!/usr/bin/env python
#-*-encoding:UTF8-*-
import os

def run(**args):
    print "[*] In dirlister module."
    files = os.listdir(".")

    return str(files)