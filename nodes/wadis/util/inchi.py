from ctypes import *
import os


def getInchiLib():
	absLibPath = ''
	try:
		path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/lib"
		absLibPath = "%s/libinchi.so.1" % path
		inchiLib = cdll.LoadLibrary(absLibPath)
	except:
		raise Exception('Could not access ' + absLibPath)
	return inchiLib



def inchiToInchiKey(inchi):
	inchiLib = getInchiLib()
	checkINCHI = inchiLib.CheckINCHI
	getStdINCHIKeyFromStdINCHI = inchiLib.GetStdINCHIKeyFromStdINCHI

	szINCHIKey = create_string_buffer(256)

	if inchi:
		check = checkINCHI(inchi, 0)
		if check >= 0:
			result = getStdINCHIKeyFromStdINCHI(inchi, szINCHIKey)
			if not result:
				return szINCHIKey.value
			else:
				raise Exception('Could not compute InChIKey from "%-s". Error code = %-d.', inchi, result)
		else:
			raise Exception('"%-s" is incorrect InChI. Error code = %d.', inchi, check)
	else:
		raise Exception('InChI is empty')




