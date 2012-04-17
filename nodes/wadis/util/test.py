from django.test.simple import DjangoTestSuiteRunner
import os
from django.conf import settings
import cProfile


class NoTestDatabaseTestRunner(DjangoTestSuiteRunner):
	def setup_databases(self, **kwargs):
		pass


	def teardown_databases(self, old_config, **kwargs):
		pass



def profile(logFile = None, sort = -1):

	if logFile and not os.path.isabs(logFile):
		logFile = os.path.join(settings.BASE_PATH, logFile)

	def decorator(func):

		def onCall(*args, **kwargs):
			prof = cProfile.Profile()
			result = None
			try:
				try:
					result = prof.runcall(func, *args, **kwargs)
				except Exception:
					pass
			finally:
				if logFile:
					prof.dump_stats(logFile)
				else:
					prof.print_stats(sort)
			return result

		return onCall

	return decorator
