class Result():

	def __init__(self, confLoader):
		self._confLoader = confLoader

	def setOneShutResults(self, oneshutResults):
		self._oneshutResults = oneshutResults

	def setCompositeResults(self, compositeResults):
		self._compositeResults = compositeResults

	def getOneShutResults(self):
		return self._oneshutResults

	def getCompositeResults(self):
		return self._compositeResults

	def getConfLoader(self): # confLoader
		return self._confLoader
