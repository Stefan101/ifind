__author__ = 'leif'
import os

PROJ_PATH = os.getcwd()
print "Project Path: %s" % (PROJ_PATH)
GAME_DB = os.path.join(PROJ_PATH,'game.db')
TEMP_PATH = os.path.join(PROJ_PATH,'templates')
STATIC_PATH = os.path.join(PROJ_PATH,'static')
MEDIA_PATH = os.path.join('')
MEDIA_URL  = '/data/'
#UPLOAD_DIR = os.path.join(PROJ_PATH,'data')
UPLOAD_DIR =  '%Y/%m/%d'

MEDIA_ROOT = 'data/'

DEPLOY = False
DEBUG = True

APP_NAME = 'pagefetch'
DATA_DIR = os.path.join(PROJ_PATH,'data')
