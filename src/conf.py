class Conf:

	def __init__(self, logConfPath, mainConfPath):
		self._logConfPath = logConfPath
		self._mainConfPath = mainConfPath

	def getMainConfPath(self):
		return self._mainConfPath

	def getLogConfPath(self):
		return self._logConfPath
