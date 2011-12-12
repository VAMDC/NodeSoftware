
class Result:
	def __init__(self):
		self.header = {}
		self._headerFields = {	'Truncated':None, 
								'count-sources':None,
								'count-species':None,
								'count-states':None,
								'count-radiative':None,
								'count-collisions' : None
							}
		self.data = {}
		self._dataFields = {'RadTrans':None,
							'Atoms':None,
							'Environments':None,
							'Particles' : None,
							'Sources':None,
							'Methods':None,
							'Functions':None,
							'CollTrans':None
							}
		
	def addHeaderField(self, key, value):
		if key in self._headerFields :
			self.header[key] = value
		else : 
			raise Exception('unknow key for header')
		
	def addDataField(self, key, value):
		if key in self._dataFields :
			self.data[key] = value
		else:
			raise Exception('unknown key for data')
			
	def getResult(self):
		headerinfo = {}
		result = {}
		for key in self.header :
			headerinfo[key] = self.header[key]
			
		result['HeaderInfo'] = headerinfo
		for key in self.data :
			result[key] = self.data[key]
			
		return result