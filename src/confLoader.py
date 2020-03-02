import json
from jsonschema import validate
# from conf import Conf

class ConfLoader:

	def __init__(self, c):
		cPath = c.getMainConfPath()
		lPath = c.getLogConfPath()
		mainconfschemaPath = './res/mainconfschema.json'
		logconfschemaPath = './res/logconfschema.json'

		mainconfschema = None
		logconfschema = None

		with open(mainconfschemaPath) as mainConfSchema:
			mainconfschema = json.load(mainConfSchema)

		with open(logconfschemaPath) as logConfSchema:
			logconfschema = json.load(logConfSchema)

		with open(cPath) as mainConf:
			self._mainConfJson = json.load(mainConf)
			validate(instance=self._mainConfJson, schema=mainconfschema)

		with open(lPath) as logConf:
			self._logConfJson = json.load(logConf)
			validate(instance=self._logConfJson, schema=logconfschema)


	def getTargetPathList(self):
		return self._logConfJson['targets']


	def getOneShutRule(self):
		return self._mainConfJson['OneShutRule']


	def getCompositRule(self):
		return self._mainConfJson['CompositeRule']

