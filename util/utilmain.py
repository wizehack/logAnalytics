import sys, getopt, os
import subprocess
import json
from httpdwnldr import HttpDwnldr
from tar import Tar

def printGuide():
	print ('python3 utilmain.py -u <download url> -s <download directory path> -t <conf file template>')
	print('or')
	print ('python3 utilmain.py -c <compressed file path> -d <destination directory path> -t <conf file template>')
	print('or')
	print ('python3 utilmain.py -d <destination directory path> -t <conf file template>')


def uncompress(srcfile, destpath):
	tar = Tar(sourcefile, sourcedir)

	if tar.zxvf() == False:
		print("Error: Can not uncompress downloaded file")
		printGuide()


def genLogConf(destDir, templateFilePath):
	print('load template....', templateFilePath)
	templateJson = None
	try:
		with open(templateFilePath) as templateFile:
			templateJson = json.load(templateFile)
	except OSError as e:
		print(e)

	if templateJson is not None:
		pathList = templateJson['path']

	logfileList = []
	for d in pathList:
		path = destDir + '/' + d
		print('log file:', path)
		logfileList.append(path)
	confData = { 'targets': logfileList}
	# print(confData)

	logConfFile = destdir + '/logconf.json'
	logConfDataFile = open(logConfFile, "w")
	logConfDataFile.write(json.dumps(confData, indent=4, sort_keys=True))
	logConfDataFile.close()

	print(logConfFile, ' is generated')


def unzip(ziplist):
	for d in zipList:
		cmd = 'gzip -d ' + d
		result = subprocess.check_output (cmd, shell=True)
		print(result)

def getAllFileList(directory, endStr, notEndStr):
	# print ('dir: ', directory)
	fileList = []
	for x in os.walk(directory):
		print('walk: ', x[0])
		for file in os.listdir(x[0]):
			if not file.endswith(notEndStr):
				if file.endswith(endStr):
					fpath = os.path.join(x[0], file)
					print(fpath)
					fileList.append(fpath)

	return fileList


if __name__ == "__main__":
	downloadurl = None
	sourcedir = None
	sourcefile = None
	compressedfile = None
	destdir = None
	template = None

	try:
		opts, args = getopt.getopt(sys.argv[1:],"hu:s:c:d:t:",["download-url=","source-dir=", "compressed-file", "dest-dir", "template"])
	except getopt.GetoptError:
		print("Error: Invalid options")
		printGuide()
		sys.exit(-1)

	for opt, arg in opts:
		if opt == '-h':
			printGuide()
			sys.exit(0)
		elif opt in ("-u", "--download-url"):
			downloadurl = arg
		elif opt in ("-s", "--source-dir"):
			sourcedir = arg
		elif opt in ("-c", "--compressed-file"):
			compressedfile = arg
		elif opt in ("-d", "--dest-dir"):
			destdir = arg
		elif opt in ("-t", "--template"):
			template = arg

	if template is None:
		print('Error: Can not find template file')
		printGuide()
		sys.exit(-1)


	if compressedfile is not None:
		if destdir is not None:
			uncompress(compressedfile, destdir)
			# tarList = getAllFileList(destdir, '.tar.gz')
			zipList = getAllFileList(destdir, '.gz','.tar.gz')
			# print (zipList)
			unzip(zipList)
			genLogConf(destdir, template)
			sys.exit(0)
		else:
			print ('Error: Can not find destination directory path')
			printGuide()
			sys.exit(-1)

	elif downloadurl is not None:
		if sourcedir is not None:
			dwnfilename = downloadurl.split('/')[-1]
			sourcefile = sourcedir + '/' + dwnfilename

			dwnldr = HttpDwnldr(downloadurl, sourcefile)

			if dwnldr.download() == False:
				print("Error: download failed")
				sys.exit(-1)

			uncompress(compressedfile, destdir)
			# tarList = getAllFileList(destdir, '.tar.gz')
			zipList = getAllFileList(destdir, '.gz','.tar.gz')
			# print (zipList)
			unzip(zipList)
			genLogConf(destdir, template)
			sys.exit(0)
		else:
			print("Error: can not find download directory path")
			printGuide()
			sys.exit(-1)

	elif destdir is not None:
		# tarList = getAllFileList(destdir, '.tar.gz')
		zipList = getAllFileList(destdir, '.gz','.tar.gz')
		# print (zipList)
		unzip(zipList)
		genLogConf(destdir, template)
		sys.exit(0)

	printGuide()
