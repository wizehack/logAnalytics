class Conf:

	def __init__(self, logConfPath, mainConfPath):
		# self._displayLogType = None
		self._logConfPath = logConfPath
		self._mainConfPath = mainConfPath

	# def setDisplyLogType(self, logType):
	#	self._displayLogType = logType

	def getMainConfPath(self):
		return self._mainConfPath

	def getLogConfPath(self):
		return self._logConfPath

	# def getDisplayLogType(self):
	#	return self._displayLogType
