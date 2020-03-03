from abc import ABC, abstractmethod
from confLoader import ConfLoader
from result import Result
import re
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
				with open(filename, 'r') as file:
					# print('========= check: ', filename)
					for line in file:
						rule = self.checkByOneshutRule(line)
						if rule:
							# print('======== catched: ', (rule['id'], line, rule['result'], rule['outputType']))
							log.append( (rule['id'], line, rule['result'], rule['outputType']) )
			except FileNotFoundError as e:
				print(e)

			if len(log) > 1:
				oneshutRes.append(log)

		# print('========= Composite Analysis ============')
		compositeRes = self.checkByCompositRule(oneshutRes)
		# print(logs)
		res = Result()
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
				# print('========= regexpr: ', regexpr)
				p = re.compile(regexpr)
				matchObj = p.search(line)

				if matchObj != None:
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
				if self.checkBooleanExpr(rule, oneshutRes):
					compositeRes.append(rule)
			elif ruleType == 'SEQUENCIAL':
				pass
			else:
				print('Not support composite rule type, please check your conf file')

		if len(compositeRes) > 0:
			# print('==== composit Result: ', compositeRes)
			return compositeRes
		else:
			return None


	def checkBooleanExpr(self, rule, oneshutRes):
		# print('======== oneshutRes: ', oneshutRes)
		# print('======== compositRule: ', rule)

		oneshutResultList = []
		for d in oneshutRes:
			oneshutResultList = oneshutResultList + d[1:]

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

