from django.db import connections


class MultipleDBRouter(object):
	def db_for_read(self, model, **hints):
		try:
			database = model.__module__.split('.')[-1]
			if database in connections:
				return database
		except IndexError:
			pass
		return None


	def db_for_write(self, model, **hints):
		try:
			database = model.__module__.split('.')[-1]
			if database in connections:
				return database
		except IndexError:
			pass
		return None


	def allow_relation(self, obj1, obj2, **hints):
		try:
			database1 = obj1.__module__.split('.')[-1]
			if database1 in connections:
				database2 = obj2.__module__.split('.')[-1]
				if database1 in connections:
					return database1 == database2
		except IndexError:
			pass
		return None


	def allow_migrate(self, db, app_label, model_name=None, **hints):
		try:
			if model_name:
				model = hints.get('model')
				if model:
					database = model.__module__.split('.')[-1]
					if database in connections:
						return db == database
		except (IndexError, AttributeError):
			pass
		return None
