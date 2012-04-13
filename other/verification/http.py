import check
import vamdctap
from django.http import HttpRequest, HttpResponse
from string import upper, lower

def getResult(tap, rules = None):

	if tap.format != 'verification':
		emsg = 'Currently, only FORMATs VERIFICATION and XSAMS are supported.\n'
		return vamdctap.views.tapServerError(status=400, errmsg=emsg)
	tap.request["FORMAT"] = "XSAMS"

	request = HttpRequest()
	request.META["SERVER_NAME"] = 'localhost'
	request.META["SERVER_PORT"] = '80'
	request.META["REMOTE_ADDR"] = '127.0.0.1'
	request.META["QUERY_STRING"] = ''
	request.REQUEST = {}

	for key in tap.request:
		request.REQUEST[upper(key)] = tap.request[key]

	xsamsResponse = vamdctap.views.sync(request)
	if xsamsResponse.get('VAMDC-COUNT-STATES', 0) < 1:
		return xsamsResponse

	if 'RETURN' in tap.request:
		action = lower(tap.request['RETURN'])
	else:
		action = 'all'

	if action not in ('all', 'good', 'bad'):
		action = 'all'

	ver = check.Verification(xsamsResponse.content, rules)
	ver.run(bad=None if action == 'all' else True if action == 'bad' else False)

	response = HttpResponse(ver.getXML(), mimetype='text/xml')
	response._headers = xsamsResponse._headers
	return response
