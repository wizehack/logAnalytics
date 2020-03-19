from analysisStrategy import AnalysisStrategy
from confLoader import ConfLoader
from result import Result

class FaultConditionBasedDetectionStrategy(AnalysisStrategy):

	def __init__(self, conf: ConfLoader):
		self._confLoader = conf

	def perform(self) -> Result:
		return result

	def updateResult(self, result: Result) -> Result:

		oneshutFaultList = []
		compositeFaultList = []

		oneshutResults = result.getOneShutResults()

		for item in oneshutResults:
			# print(item)
			results = item[1:]
			for oneshutResultTuple in results:
				if oneshutResultTuple[4] == 'FAULT':
					oneshutFaultList.append(oneshutResultTuple)

		result.setOneshutFaultList(oneshutFaultList)

		compositeResults = result.getCompositeResults();

		if compositeResults:
			for item in compositeResults:
				if item['logType'] == 'FAULT':
					compositeFaultList.append(item)

			result.setCompositeFaultList(compositeFaultList)

		# print('composit: ', compositeFaultList)
		return result
