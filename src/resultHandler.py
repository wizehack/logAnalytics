from abc import ABC, abstractmethod
from result import Result

class Handler(ABC):

	@abstractmethod
	def setNext(self, nextHandler):
		pass

	@abstractmethod
	def show(self, res):
		pass


class ResultHandler(Handler):

	_next = None

	def setNext(self, nextHandler) -> Handler:
		self._next = nextHandler
		return nextHandler

	def show(self, res: Result):
		if self._next:
			return self._next.show(res)
		else:
			print('N/A')
		return 'OK bye`~~'

	def printFile(self, path: str):
		try:
			with open(path, 'r') as file:
				for line in file:
					print(line)

		except FileNotFoundError as e:
			print(e)


class OneshutFileResultHandler(ResultHandler):

	_displayedRule = []

	def show(self, res: Result) -> str:
		print('==== Applying Oneshut Rule by FILE type ====')
		oneshutResults = res.getOneShutResults()

		for item in oneshutResults:
			filename = item[0]
			results = item[1:]

			for d in results:
				if d[3] == 'FILE':
					if d[0] in self._displayedRule:
						print(d[0], d[1])
					else:
						self._displayedRule.append(d[0])
						print('Log File: ', filename)
						print('Rule ID: ', d[0])
						print('Log Line: ')
						print(d[1])
						print('Analysis Result')
						super().printFile(d[2])
						print('\n\n')

		return super().show(res)


class OneshutTextResultHandler(ResultHandler):

	_displayedRule = []

	def show(self, res: Result) -> str:
		print('==== Applying Oneshut Rule by TEXT type ====')
		oneshutResults = res.getOneShutResults()

		for item in oneshutResults:
			filename = item[0]
			results = item[1:]

			for d in results:
				if d[3] == 'TEXT':
					if d[0] in self._displayedRule:
						print(d[0], d[1])
					else:
						self._displayedRule.append(d[0])
						print('Log File: ', filename)
						print('Rule ID: ', d[0])
						print('Log Line: ')
						print(d[1])
						print('Analysis Result')
						print(d[2])
						print('\n\n')

		return super().show(res)


class CompositeFileResultHandler(ResultHandler):

	def show(self, res: Result) -> str:
		print('==== Applying Composite Rule by FILE type ====')
		compositeResults = res.getCompositeResults()

		if compositeResults:
			for item in compositeResults:
				if(item['outputType'] == 'FILE'):
					print('ID : ', item['id'])
					print('Rule type: ', item['ruleType'])

					if item['ruleType'] == 'BOOLEANEXPR':
						print('Condition: ', item['condition'])

						print('Result')
						super().printFile(item['result'])
						print('\n\n')

		return super().show(res)


class CompositeTextResultHandler(ResultHandler):

	def show(self, res: Result) -> str:
		print('==== Applying Composite Rule by TEXT type ====')
		compositeResults = res.getCompositeResults()

		if compositeResults:
			for item in compositeResults:
				if(item['outputType'] == 'TEXT'):
					print('ID : ', item['id'])
					print('Rule type: ', item['ruleType'])

					if item['ruleType'] == 'BOOLEANEXPR':
						print('Condition: ', item['condition'])

					print('Result')
					print(item['result'])
					print('\n\n')

		return super().show(res)
