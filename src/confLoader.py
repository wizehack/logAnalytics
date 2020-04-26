import json
from jsonschema import validate

class ConfLoader:

	def __init__(self, c):
		self._conf = c
		self._mainConfJson = None
		self._logConfJson = None

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
			with open(self._conf.getMainConfPath()) as mainConf:
				self._mainConfJson = json.load(mainConf)
				validate(instance=self._mainConfJson, schema=mainconfschema)

		except FileNotFoundError as e:
			print(e)

		try:
			print("confPath: ", self._conf.getLogConfPath())
			with open(self._conf.getLogConfPath()) as logConf:
				self._logConfJson = json.load(logConf)
				validate(instance=self._logConfJson, schema=logconfschema)

		except FileNotFoundError as e:
			print(e)



	def getTargetPathList(self):
		print(" getTargetPathList:", self._logConfJson)
		if self._logConfJson:
			return self._logConfJson['targets']
		return None


	def getOneShutRule(self):

		if self._mainConfJson:
			return self._mainConfJson['OneShutRule']
		return None


	def getCompositeRule(self):

		if self._mainConfJson:
			return self._mainConfJson['CompositeRule']
		return None

'''
	def getDisplayLogType(self):
		return self._conf.getDisplayLogType()
	'''
