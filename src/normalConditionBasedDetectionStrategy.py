from analysisStrategy import AnalysisStrategy
from confLoader import ConfLoader
from result import Result

class NormalConditionBasedDetectionStrategy(AnalysisStrategy):

	def __init__(self, conf: ConfLoader):
		self._confLoader = conf

	def perform(self) -> Result:
		return result

	def updateResult(self, result: Result) -> Result:
		detectedRule = self.detectViolatedCompositeRule(result)
		# print('===detectedRule: ', detectedRule)
		oneshutRes = result.getOneShutResults()
		# print('oneshutRes:', oneshutRes)

		ruleList = []
		for rule in detectedRule:
			if rule['ruleType'] == 'BOOLEANEXPR':
				conditionStr = rule['condition']
				logs = []
				for resultTuple in oneshutRes:
					for d in resultTuple[1:]: # remove filepath`
						#print(conditionStr, '>>> ', d[0])
						if conditionStr.find(d[0]) > -1: # item[0] is id
							logs.append(d)
							rule["logs"] = logs
							##print('=== ', rule)
							ruleList.append(rule)
							#print(ruleList)
			elif rule['ruleType'] == 'SEQUENTIAL':
				idSeqList = rule['order']
				logs = []

				for idStr in idSeqList:
					for resultTuple in oneshutRes:
						for d in resultTuple[1:]: # remove filepath`
							if d[0] == idStr:
								logs.append(d)
								rule["logs"] = logs
								ruleList.append(rule)

		result.setCompositeViolatedRule(ruleList)

		return result

	def detectViolatedCompositeRule(self, result:Result) -> list:
		compositeNormalTypeList = []
		detectedRule = []
		normalIdTuple = None

		confLoader = result.getConfLoader()

		compositeResults = result.getCompositeResults();
		# print('==== compositeResults:', compositeResults)

		if compositeResults:
			for item in compositeResults:
				if item['logType'] == 'NORMAL':
					compositeNormalTypeList.append(item)

		if compositeNormalTypeList:
			normalIdTuple = tuple(item['id'] for item in compositeNormalTypeList)

		compositeRule = self._confLoader.getCompositeRule()
		# print(compositeRule)

		if compositeRule:
			for item in compositeRule:
				if item['logType'] == 'NORMAL':
					if normalIdTuple:
						if not item['id'] in normalIdTuple:
							detectedRule.append(item)

		return detectedRule
