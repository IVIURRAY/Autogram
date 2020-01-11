import os
import tempfile

TEMP_DIR = os.path.normpath(tempfile.gettempdir() + '/Autogram')
POSTS_DIR = os.path.normpath(TEMP_DIR + '/posts')
ARCHIVE_DIR = os.path.normpath(TEMP_DIR + '/.archive')
SCHEDULE = os.path.normpath(TEMP_DIR + '/.schedule')