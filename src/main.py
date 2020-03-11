import sys, getopt
from ruleBasedStrategy import RuleBasedStrategy
from faultConditionBasedDetectionStrategy import FaultConditionBasedDetectionStrategy
from normalConditionBasedDetectionStrategy import NormalConditionBasedDetectionStrategy
from analyzer import LogAnalyzer
from analyzer import FaultDetector
from confLoader import ConfLoader
from resultHandler import OneshutResultHandler
from resultHandler import CompositeResultHandler
from oneshutViolatedRuleHandler import OneshutViolatedRuleHandler
from compositeViolatedRuleHandler import CompositeViolatedRuleHandler
from conf import Conf

def checkOption(argv):
	logconf = ''
	mainconf = ''

	try:
		opts, args = getopt.getopt(argv,"hl:c:",["lfile=","cfile="])
	except getopt.GetoptError:
		print ('error: python main.py -l <logconf.json> -c <mainconf.json>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print ('python main.py -l <logconf.json> -c <mainconf.json>')
			sys.exit()
		elif opt in ("-l", "--lfile"):
			logconf = arg
		elif opt in ("-c", "--cfile"):
			mainconf = arg
	print ('log conf file is ', logconf)
	print ('main conf file is ', mainconf)

	conf = Conf(logconf, mainconf)

	return conf


if __name__ == "__main__":

	#setup chain of responsibility
	oneshutResultHandler = OneshutResultHandler()
	compositeResultHandler = CompositeResultHandler()
	oneshutViolatedRuleHandler = OneshutViolatedRuleHandler()
	compositeViolatedRuleHandler = CompositeViolatedRuleHandler()

	handler = oneshutResultHandler.setNext(compositeResultHandler)
	handler = handler.setNext(oneshutViolatedRuleHandler)
	handler = handler.setNext(compositeViolatedRuleHandler)

	confTemp = checkOption(sys.argv[1:])
	cLoader = ConfLoader(confTemp)

	logAnalyzer = LogAnalyzer(RuleBasedStrategy(cLoader))
	result = logAnalyzer.execute()

	faultDetector = FaultDetector(result, FaultConditionBasedDetectionStrategy(cLoader))
	result = faultDetector.execute()

	faultDetector = FaultDetector(result, NormalConditionBasedDetectionStrategy(cLoader))
	result = faultDetector.execute()
	print(oneshutResultHandler.show(result))

