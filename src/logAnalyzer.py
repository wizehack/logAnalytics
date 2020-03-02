from analysisStrategy import AnalysisStrategy
from result import Result

class LogAnalyzer():

	def __init__(self, logPathList: list, strategy: AnalysisStrategy):
		self._logPathList = logPathList
		self._strategy = strategy

	def execute(self) -> Result:
		return self._strategy.perform(self._logPathList);
