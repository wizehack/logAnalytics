from result import Result
from resultHandler import ResultHandler

class OneshutViolatedRuleHandler(ResultHandler):

	def show(self, res: Result) -> str:
		print('==== Faulty Logs ====')
		faultList = res.getOneshutFaultList()

		for item in faultList:
			#print('fault: ', item)
			#ruleId = item[0]
			logLine = item[1]
			analysisResult = item[2]
			resultType = item[3]
			# print(results)

			if resultType == 'TEXT':
				# print('Rule ID: ', ruleId)
				print(logLine)
				print('\n\n')

		return super().show(res)

