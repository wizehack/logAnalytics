from analysisStrategy import AnalysisStrategy
from result import Result

class LogAnalyzer():

	def __init__(self, strategy: AnalysisStrategy):
		self._strategy = strategy

	def execute(self) -> Result:
		return self._strategy.perform();

class FaultDetector():

	def __init__(self, result: Result, strategy: AnalysisStrategy):
		self._result = result
		self._strategy = strategy

	def execute(self) -> Result:
		return self._strategy.updateResult(self._result)
