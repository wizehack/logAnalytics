class Result():

	def __init__(self, confLoader):
		self._confLoader = confLoader
		self._oneshutResults = None
		self._compositeResults = None
		self._oneshutFaultList = None
		self._compositeFaultList = None
		self._compositeViolatedRule = None

	def setOneShutResults(self, oneshutResults):
		self._oneshutResults = oneshutResults

	def setCompositeResults(self, compositeResults):
		self._compositeResults = compositeResults

	def setOneshutFaultList(self, faultList):
		self._oneshutFaultList = faultList

	def setCompositeFaultList(self, faultList):
		self._compositeFaultList = faultList

	# def setOneshutViolatedRule(self, rule):
	# 	self._oneShutViolatedRule = rule

	def setCompositeViolatedRule(self, rule):
		self._compositeViolatedRule = rule

	def getOneShutResults(self):
		return self._oneshutResults

	def getCompositeResults(self):
		return self._compositeResults

	def getOneshutFaultList(self):
		return self._oneshutFaultList

	def getCompositeFaultList(self):
		return self._compositeFaultList

	# def getOneshutViolatedRule(self):
	# 	return self._oneShutViolatedRule

	def getCompositeViolatedRule(self):
		return self._compositeViolatedRule

	def getConfLoader(self): # confLoader
		return self._confLoader
