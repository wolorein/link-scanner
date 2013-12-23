import yara
import sys
import hashlib
import os
import socket
from urllib2 import urlopen, URLError, HTTPError

#################################################
#				YARA SCAN FUNCTIONS				#
#################################################
def scanfile(filename):
	rtext = loadrs("static", ".yara")
	if not rtext:
		print "----> No rules found! <----"
		return 0
	rules = yara.compile(source=rtext)
	matches = rules.match(filename)
	if not matches:
		print "----> Scan result: OK <----"
		return 1
	else:
		print "----> Scan result: Warning! <----"
		printmatches(matches)
		return 0
			
#Load rule files into a string
def loadrs(dir, ends):
	rulestext = ""
	line = ""
	for r,d,f in os.walk(dir):
		for files in f:
			if files.endswith(ends):
				fname = open(os.path.join(r, files))
				line = fname.readline()
				while (line):
					rulestext += line
					line = fname.readline()
				fname.close()
	return rulestext
	
#################################################
#				HASH FUNCTIONS					#
#################################################
def hashforfile(file):
	chunk_size = 1048576
	md5 = hashlib.md5()
	sha256 = hashlib.sha256()
	f = open(file, 'rb')
	data = f.read(chunk_size)
	while data:
		md5.update(data)
		sha256.update(data)
		data = f.read(chunk_size)
	f.close()
	print('MD5: ' + md5.hexdigest())
	print('SHA256: ' + sha256.hexdigest())

#################################################
#				URLLIB2 DOWNLOAD				#
#################################################
def downloadurl(todir, url):	
	try:
		u = urlopen(url, timeout = 1)
		print "Opening: " + url
	except Exception, e:
		print "Error during url open."
		return (0, "Error")
		
	file_name = url.split('/')[-1]
	openpath = os.path.join(todir, file_name)
	f = open(openpath, 'wb')

	file_size_dl = 0
	block_sz = 8192
	buffer = u.read(block_sz)
	while buffer:
		file_size_dl += len(buffer)
		f.write(buffer)
		status = r"%10d" % file_size_dl
		status = status + chr(8)*(len(status)+1)
		print status,
		buffer = u.read(block_sz)
	f.close()
	print "\n"
	hashforfile(openpath)
	if scanfile(openpath):
		return (1, url)
	else: 
		return (0, "Yara warning, sucpicious file!")
	
#downloadurl("download", "http://letoltes.szoftverbazis.hu/1S0Qx0b3tI_VveR8gUXoKw/1388394249/q-dir-585/Q-Dir_Installer.exe")
