import sys, getopt
from analysisStrategy import RuleBasedStrategy
from logAnalyzer import LogAnalyzer
from confLoader import ConfLoader
from resultHandler import OneshutFileResultHandler
from resultHandler import OneshutTextResultHandler
from resultHandler import CompositeFileResultHandler
from resultHandler import CompositeTextResultHandler
from conf import Conf

def checkOption(argv):
	logconf = ''
	mainconf = ''
	logType= None

	try:
		opts, args = getopt.getopt(argv,"hl:c:f:",["lfile=","cfile=", "logType="])
	except getopt.GetoptError:
		print ('error: python main.py -l <logconf.json> -c <mainconf.json> -f <NORMAL, FAULT>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print ('python main.py -l <logconf.json> -c <mainconf.json>')
			sys.exit()
		elif opt in ("-l", "--lfile"):
			logconf = arg
		elif opt in ("-c", "--cfile"):
			mainconf = arg
		elif opt in ("-f", "--logType"):
			logType = arg
	print ('log conf file is ', logconf)
	print ('main conf file is ', mainconf)
	print ('logType is  ', logType)

	conf = Conf(logconf, mainconf)

	if logType:
		conf.setDisplyLogType(logType)

	return conf


if __name__ == "__main__":

	#setup chain of responsibility
	oneshutFileHandler = OneshutFileResultHandler()
	oneshutTextHandler = OneshutTextResultHandler()
	compositeFileHandler = CompositeFileResultHandler()
	compositeTextHandler = CompositeTextResultHandler()
	oneshutFileHandler.setNext(oneshutTextHandler).setNext(compositeFileHandler).setNext(compositeTextHandler)

	confTemp = checkOption(sys.argv[1:])
	cLoader = ConfLoader(confTemp)
	logPathList = cLoader.getTargetPathList()

	analyzer = LogAnalyzer(logPathList, RuleBasedStrategy(cLoader))
	result = analyzer.execute()

	print(oneshutFileHandler.show(result))

