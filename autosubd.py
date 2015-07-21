#!/usr/bin/env python
import urllib
import gzip
import sys, os, glob, struct
import xmlrpclib
from settings import Settings
from opensub import OpenSubtitle
from fileutils import File

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def search_sub(filename):
	f=File(path+filename)
	content = [{'sublanguageid':language,'moviebytesize':f.size ,'moviehash':f.get_hash()}]
	try:
		datarcv = Os1.search_subs(content)
		downlink = datarcv['data'][0]['SubDownloadLink']

		#Downloading zip file
		urllib.urlretrieve(downlink, 'subtemp.gz')

		#Unzip de subtitle file in directory
		inF = gzip.GzipFile('subtemp.gz', 'rb')
		s = inF.read()
		inF.close()
		filenamesrt = filename[0:len(filename)-4] + '.' + language_ext + '.srt'
		outF = file(path+filenamesrt, 'wb')
		outF.write(s)
		outF.close()
		print fn + ' -> ' + bcolors.OKGREEN + 'Download OK' + bcolors.ENDC
	except:
		print fn + ' -> ' + bcolors.WARNING + 'No subtitle found' + bcolors.ENDC

#select mode: with arguments or without them
#argment 1: directory or file, argument 2: language
if len(sys.argv) < 3:
	language = Settings.language
else:
	language = sys.argv[2]
if len(sys.argv) < 2:
	path = Settings.path
else:
	path = sys.argv[1]
	if sys.argv[1] == 'help':
		print 'autosubd.py [search path] [language]'
		sys.exit()

#because the previous version of my software did this:
#Spanish:Para que sea compatible con la anterior version (Los subtitulos se guardaban con 'es')		
if language == 'spa':
	language_ext = 'es'
else:
	language_ext = language

Os1 = OpenSubtitle()
print Os1.login()
try:
	os.chdir(path)
except:
	#Mode: one file
	if os.path.isfile(path):
		[path,fn] = os.path.split(path)
		path = path + '/'
		print 'Searching subtitle for ' + path + fn
		os.chdir(path)
		search_sub(fn)
	Os1.logout()
	if os.path.exists('subtemp.gz'):
		os.remove('subtemp.gz')
	sys.exit()

#Modo: files in directory
print 'Looking for video files in ' + path
types = Settings.filetypes
for ext in types:
    for fn in glob.glob('*.' + ext)+glob.glob('*/*.'+ext)+glob.glob('*/*/*.'+ext)+glob.glob('*/*/*/*.'+ext):
        filenamesrt = fn[0:len(fn)-4] + '.' + language_ext +  '.srt'
        if not os.path.exists(filenamesrt):
        	#print 'File: ' + fn
        	#print '->Downloading subtitle...'
    		search_sub(fn)

Os1.logout()

if os.path.exists('subtemp.gz'):
	os.remove('subtemp.gz')


