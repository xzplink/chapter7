#!/usr/bin/env python
#-*-encoding:UTF8-*-
import os

def run(**args):
    print "[*] In environmnet module."
    return str(os.environ)