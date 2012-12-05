class Result:
	def __init__(self):
		self.header = {}
		self._headerFields = {	'COUNT-SOURCES':None,
                                'COUNT-ATOMS' : None,
                                'COUNT-MOLECULES':None,
								'COUNT-SPECIES':None,
								'COUNT-STATES':None,
								'COUNT-RADIATIVE':None,
								'COUNT-COLLISIONS' : None,
                                'COUNT-NONRADIATIVE':None,
                                'TRUNCATED':None,
                                'APPROX-SIZE':None  
							}
		self.data = {}
		self._dataFields = {'RadTrans':None,
                            'Molecules':None,
							'Atoms':None,
							'Environments':None,
							'Particles' : None,
							'Sources':None,
							'Methods':None,
							'Functions':None,
							'CollTrans':None,
                            'RadCross':None
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

class State():
    def __init__(self):
        self.Components = []
        self.Sources = []
        self.id = None
        self.totalAngularMomentum = None


class Shifting():
    def __init__(self):
        self.environment = None
        self.name = None
        self.ShiftingParams = list()   

class ShiftingParameter():
    def __init__(self):
        self.value = None
        self.accurracy = None        
        self.comment = None
        
class LineshapeParameter():
    def __init__(self):
        self.environment = None
        self.value = None
        self.accurracy = None
        self.name = None
        self.comment = None
