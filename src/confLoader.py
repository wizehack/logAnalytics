import json
from jsonschema import validate

class ConfLoader:

	def __init__(self, c):
		cPath = c.getMainConfPath()
		lPath = c.getLogConfPath()
		mainconfschemaPath = './res/mainconfschema.json'
		logconfschemaPath = './res/logconfschema.json'

		mainconfschema = None
		logconfschema = None

		try:
			with open(mainconfschemaPath) as mainConfSchema:
				mainconfschema = json.load(mainConfSchema)

		except FileNotFoundError as e:
			print(e)

		try:
			with open(logconfschemaPath) as logConfSchema:
				logconfschema = json.load(logConfSchema)

		except FileNotFoundError as e:
			print(e)

		try:
			with open(cPath) as mainConf:
				self._mainConfJson = json.load(mainConf)
				validate(instance=self._mainConfJson, schema=mainconfschema)

		except FileNotFoundError as e:
			print(e)

		try:
			with open(lPath) as logConf:
				self._logConfJson = json.load(logConf)
				validate(instance=self._logConfJson, schema=logconfschema)

		except FileNotFoundError as e:
			print(e)


	def getTargetPathList(self):
		return self._logConfJson['targets']


	def getOneShutRule(self):
		return self._mainConfJson['OneShutRule']


	def getCompositRule(self):
		return self._mainConfJson['CompositeRule']

