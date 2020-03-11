from abc import ABC, abstractmethod
from confLoader import ConfLoader
from result import Result

class AnalysisStrategy(ABC):

	@abstractmethod
	def __init__(self, conf: ConfLoader):
		pass


	@abstractmethod
	def perform(self) -> Result:
		pass


	@abstractmethod
	def updateResult(self, result: Result) -> Result:
		pass
