from abc import ABC, abstractmethod
from confLoader import ConfLoader
from result import Result
import re
import codecs
#from logHandle import LogHandle

class AnalysisStrategy(ABC):

	@abstractmethod
	def __init__(self, conf: ConfLoader):
		pass


	@abstractmethod
	def perform(self, logPathList: list) -> Result:
		pass


class RuleBasedStrategy(AnalysisStrategy):

	def __init__(self, conf: ConfLoader):
		self._confLoader = conf

	def perform(self, logPathList: list) -> Result:
		oneshutRes = []
		# print('========= Oneshut Analysis ============')
		for n in range(len(logPathList)):
			filename = logPathList[n]
			# print('======= tracking: ', filename)

			log = [filename,]
			try:
				with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as fdata:
					# print('========= check: ', filename)
					try:
						for line in fdata:
							rule = self.checkByOneshutRule(line)
							if rule:
								# print('======== catched: ', (rule['id'], line, rule['result'], rule['outputType']))
								log.append( (rule['id'], line, rule['result'], rule['outputType'], rule['logType']) )
					except UnicodeDecodeError as e2:
						print(filename, line, e2)

			except FileNotFoundError as e1:
				print(e1)

			if len(log) > 1:
				oneshutRes.append(log)

		# print('========= Composite Analysis ============')
		compositeRes = self.checkByCompositRule(oneshutRes)
		# print(logs)
		res = Result(self._confLoader)
		res.setOneShutResults(oneshutRes)
		res.setCompositeResults(compositeRes)

		return res

	def checkByOneshutRule(self, line):
		# print('========= line: ', line)
		rules = self._confLoader.getOneShutRule();
		for n in range(len(rules)):
			filters = rules[n]['filter']

			bFound = True
			for i in range(len(filters)):
				regexpr = filters[i]
				#print('========= regexpr: ', regexpr)
				p = re.compile(regexpr)
				matchObj = p.search(line)

				if matchObj != None:
					# print('========= regexpr: ', regexpr, line)
					value = matchObj.group()
					if value:
						# print('======= matched: ', value)
						bFound = bFound and True
					else:
						bFound = bFound and False
						break
				else:
					bFound = bFound and False
					break

			if True == bFound:
				return rules[n]
		return None


	def checkByCompositRule(self, oneshutRes):
		rules = self._confLoader.getCompositRule();
		compositeRes = []

		for rule in rules:
			ruleType = rule['ruleType']
			if ruleType == 'BOOLEANEXPR':
				if self.isMatchedByBooleanExpr(rule, oneshutRes):
					compositeRes.append(rule)
			elif ruleType == 'SEQUENTIAL':
				# print("======= rule: ", rule)
				if self.isMatchedByOrder(rule, oneshutRes):
					compositeRes.append(rule)
			else:
				print('Not support composite rule type, please check your conf file')

		if len(compositeRes) > 0:
			# print('==== composit Result: ', compositeRes)
			return compositeRes
		else:
			return None


	def isMatchedByBooleanExpr(self, rule, oneshutRes):
		# print('======== oneshutRes: ', oneshutRes)
		# print('======== compositRule: ', rule)

		oneshutResultList = []
		for d in oneshutRes:
			oneshutResultList = oneshutResultList + d[1:] # remove filepath

		oneshutRules = self._confLoader.getOneShutRule();
		oneshutIdTuple = tuple(oneshut['id'] for oneshut in oneshutRules)
		oneshutResultIdTuple = tuple (item[0] for item in oneshutResultList)
		# print('======= oneshutResultIdTuple: ', oneshutResultIdTuple)

		boolValue = None
		conditionStr = rule['condition']
		for oneshutId in oneshutIdTuple:
			if oneshutId in oneshutResultIdTuple:
				boolValue = 'True'
			else:
				boolValue = 'False'

			conditionStr = conditionStr.replace(oneshutId, boolValue)

		# print('========== condition: ', conditionStr)
		return eval(conditionStr)

	def isMatchedByOrder(self, rule, oneshutRes):
		oneshutResultList = []
		for d in oneshutRes:
			oneshutResultList = oneshutResultList + d[1:] # remove filepath

		oneshutRules = self._confLoader.getOneShutRule();
		oneshutIdTuple = tuple(oneshut['id'] for oneshut in oneshutRules)
		oneshutResultIdTuple = tuple (item[0] for item in oneshutResultList)

		orderCond = rule['order']

		maxnum = -1
		for d in orderCond:
			num = self.getSequenceNum(d, oneshutIdTuple)
			# print("======= order num: ", num)

			if num > len(oneshutIdTuple):
				return False

			if num > maxnum:
				num = maxnum
			else:
				return False

		return True


	def getSequenceNum(self, item, oneshutIdTuple):
		# print("======= ", item)

		for n in range(len(oneshutIdTuple)):
			if item == oneshutIdTuple[n]:
				return n

		return len(oneshutIdTuple) + 1

