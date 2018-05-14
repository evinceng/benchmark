# -*- coding: utf-8 -*-
"""
Created on Mon May 14 15:29:45 2018

@author: evin
"""

from ConfigParser import ConfigParser
import os

DEFAULT_CONFIG_FILE = 'config.ini'

def getConfigFile():
    return os.environ.get('CONFIG_FILE', DEFAULT_CONFIG_FILE)

CONFIG_FILE = getConfigFile()

def createConfig(configFile=None):
    parser = ConfigParser()
    parser.read(configFile or CONFIG_FILE)
    return parser

CONFIG = createConfig()

def getConfig():
    return CONFIG