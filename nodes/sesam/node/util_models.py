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
							'Atoms':None,
                            'Molecules':None,
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
        
class Methods:
    def __init__(self):
        self._methodsDict = self.__initMethods()
        self._methodsList = self.__dictToList(self._methodsDict)
        
    def getMethodsAsList(self):
        return self._methodsList

    def getMethodsAsDict(self):
        return self._methodsDict
        
    def getMethodFromDict(self, method):
        return self._methodsDict[method]
            
    def __initMethods(self):
        methods = {}
        obs = Method()
        obs.category = "observed"
        obs.id = 1
        methods[obs.category] = obs
        calc = Method()
        calc.category = "theory"
        calc.id = 2
        methods[calc.category] = calc
        return methods
        
    def __dictToList(self, dic):
        result = []
        for key, value in dic.items():            
            result.append(value)            
        return result
    
      
class Method(object):
    def __init(self):
        self._id = None
        self._functionRef = None
        self._category = None
        self._description = None


    @property
    def id(self):
        return self._id
        
    @id.setter
    def id(self, value):
        self._id = value
        
    @property
    def functionRef(self):
        return self._functionRef
        
    @functionRef.setter
    def functionRef(self, functionRef):
        self._functionRef = functionRef
        
    @property
    def category(self):
        return self._category
        
    @category.setter
    def category(self, category):
        self._category = category
        
    @property
    def description(self):
        return self._description
        
    @description.setter
    def description(self, description):
        self._description = description



