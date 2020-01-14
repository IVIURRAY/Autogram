import os
import tempfile

DEFAULT_USERNAME = 'no username'
DEFAULT_PASSWORD = 'no password'

TEMP_DIR = os.path.normpath(tempfile.gettempdir() + '/Autogram')
POSTS_DIR = os.path.normpath(TEMP_DIR + '/posts')
CHROME_DIR = os.path.normpath(TEMP_DIR + '/chromedriver')
ARCHIVE_DIR = os.path.normpath(TEMP_DIR + '/.archive')
SCHEDULE = os.path.normpath(TEMP_DIR + '/.schedule')