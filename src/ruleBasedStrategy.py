from analysisStrategy import AnalysisStrategy
from confLoader import ConfLoader
from result import Result
import re
import codecs

class RuleBasedStrategy(AnalysisStrategy):

	def __init__(self, conf: ConfLoader):
		self._confLoader = conf


	def updateResult(self, result: Result) -> Result:
		return result


	def perform(self) -> Result:
		oneshutRes = []
		# print('========= Oneshut Analysis ============')
		logPathList = self._confLoader.getTargetPathList()

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
		compositeRes = self.checkByCompositeRule(oneshutRes)
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


	def checkByCompositeRule(self, oneshutRes):
		self._matchedLogList = []
		rules = self._confLoader.getCompositeRule();
		compositeRes = []

		for rule in rules:
			ruleType = rule['ruleType']
			if ruleType == 'BOOLEANEXPR':
				if self.isMatchedByBooleanExpr(rule, oneshutRes):
					logs = self._matchedLogList
					rule['logs'] = logs
					compositeRes.append(rule)
			elif ruleType == 'SEQUENTIAL':
				# print("======= rule: ", rule)
				if self.isMatchedByOrder(rule, oneshutRes):
					logs = self._matchedLogList
					rule['logs'] = logs
					compositeRes.append(rule)
			else:
				print('Not support composite rule type, please check your conf file')

		if len(compositeRes) > 0:
			# print('==== composit Result: ', compositeRes)
			return compositeRes
		else:
			return None


	def isMatchedByBooleanExpr(self, rule, oneshutRes):
		self._matchedLogList = []
		# print('======== oneshutRes: ', oneshutRes)
		# print('======== compositRule: ', rule)
		oneshutResultList = []
		retValue = False
		for d in oneshutRes:
			oneshutResultList = oneshutResultList + d[1:] # remove filepath

		oneshutRules = self._confLoader.getOneShutRule();
		oneshutIdTuple = tuple(oneshut['id'] for oneshut in oneshutRules)
		oneshutMatchedIdLogTuple = tuple ((item[0],item[1]) for item in oneshutResultList)
		# print('======= oneshutMatchedIdLogTuple: ', oneshutMatchedIdLogTuple)

		boolValue = None
		conditionStrOrign = rule['condition']
		conditionStr = conditionStrOrign
		# print('========== conditionStrOrign: ', conditionStr)
		for oneshutId in oneshutIdTuple:
			for item in oneshutMatchedIdLogTuple:
				# print(oneshutId, item[0])
				if oneshutId == item[0]:
					boolValue = 'True'
					self._matchedLogList.append(item[1])
					break
				else:
					boolValue = 'False'
				conditionStr = conditionStr.replace(oneshutId, boolValue)

		# print('========== eval: ', conditionStr)
		try:
			retValue = eval(conditionStr)
		except NameError as e:
			print('[ERROR]', e, 'in the conditon:', conditionStrOrign)
			retValue = False

		return retValue


	def isMatchedByOrder(self, rule, oneshutRes):
		self._matchedLogList = []
		oneshutResultList = []
		for d in oneshutRes:
			oneshutResultList = oneshutResultList + d[1:] # remove filepath

		#oneshutRules = self._confLoader.getOneShutRule();
		# oneshutIdTuple = tuple(oneshut['id'] for oneshut in oneshutRules)
		oneshutResultIdTuple = tuple (item[0] for item in oneshutResultList)
		oneshutResultLogTuple = tuple (item[1] for item in oneshutResultList)
		orderCond = rule['order']

		# print('==== oneshutResultIdTuple: ', oneshutResultIdTuple)
		# print('==== oneshutResultLogTuple: ', oneshutResultLogTuple)
		# print('==== orderCond: ', orderCond)

		maxnum = -1
		for d in orderCond:
			num = self.getSequenceNum(d, oneshutResultIdTuple)
			# print("======= order num: ", num)

			if num > len(oneshutResultIdTuple):
				return False

			if num > maxnum:
				self._matchedLogList.append(oneshutResultLogTuple[num])
				num = maxnum
			else:
				return False

		return True


	def getSequenceNum(self, item, oneshutIdTuple):
		# print("======= ", item)

		for n in range(len(oneshutIdTuple)):
			# print("======= compare: ", oneshutIdTuple[n])
			if item == oneshutIdTuple[n]:
				return n

		return len(oneshutIdTuple) + 1

