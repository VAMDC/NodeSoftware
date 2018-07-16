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
                'APPROX-SIZE':None,
                'LAST-MODIFIED':None
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
        
        
class FunctionBuilder():
    @staticmethod
    def widthCalculation():
        f = Function()
        f.id = 1
        f.name = 'width'
        f.description="log(w)"
        f.addArg('T', 'K', 'Temperature')
        f.addParam('a0', '', '')
        f.addParam('a1', '', '')
        f.addParam('a2', '', '')
        return f
        
    @staticmethod
    def shiftCalculation():
        f = Function()
        f.id = 2
        f.name = 'shift'
        f.description="d/w"
        f.addArg('T', 'K', 'Temperature')
        f.addParam('b0', '', '')
        f.addParam('b1', '', '')
        f.addParam('b2', '', '')
        return f
        
        
class Function():
    def __init__(self):
        self.id = None
        self.comments = None
        self.name = None
        self.expression = None
        self.language = None
        self.Arguments = []
        self.Parameters = []
        
    def cleanArgs(self):
        del(self.args[:])
        
    def cleanParams(self):
        del(self.params[:])
        
    def addArg(self, name, unit, description):
        self.Arguments.append(Argument(name, unit, description))
        
    def addParam(self, name, unit, description):
        self.Parameters.append(Parameter(name, unit, description))
        
class Argument():
    def __init__(self, name, unit, descr):
        self.name = name
        self.unit = unit
        self.description = descr
    
class Parameter():
    def __init__(self, name, unit, descr):
        self.name = name
        self.unit = unit
        self.description = descr
    

class State():
    def __init__(self):
        self.Components = []
        self.Sources = []
        self.id = None
        self.totalAngularMomentum = None

class Broadenings(object):
    def __init__(self, broadenings):
        self.Broadenings = broadenings

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
