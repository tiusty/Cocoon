# Import the os module, for the os.walk function
import os, shutil

# Set the directory you want to start from
rootDir = '../../'
for dirName, subdirList, fileList in os.walk(rootDir):
    if "migrations" in dirName:
        print('Removing: %s' % dirName)
        shutil.rmtree(dirName)
