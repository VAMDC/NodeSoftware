from django.test.simple import DjangoTestSuiteRunner


class NoTestDatabaseTestRunner(DjangoTestSuiteRunner):
	def setup_databases(self, **kwargs):
		pass


	def teardown_databases(self, old_config, **kwargs):
		pass

