from result import Result
from resultHandler import ResultHandler

class CompositeViolatedRuleHandler (ResultHandler):

	def show(self, res: Result) -> str:
		print('==== Composite faulty Logs  ====')
		faultList = res.getCompositeFaultList()

		if faultList:
			for item in faultList:
				print('Rule ID', item['id'])

			logList = item['logs']
			for d in logList:
				print(d)
				print('\n\n')

		print('==== Detected abnomal states ====')
		abnormalList = res.getCompositeViolatedRule()

		if abnormalList:
			for item in abnormalList:
				print('Rule ID', item['id'])

			if item['ruleType'] == 'BOOLEANEXPR':
				print('Condition: ', item['condition'])
			elif item['ruleType'] == 'SEQUENTIAL':
				print('order: ', item['order'])

			logList = item['logs']
			print('\nRemained logs')
			for d in logList:
				print(d[1])
				print('\n\n')

		#print(abnormalList)

		return super().show(res)
