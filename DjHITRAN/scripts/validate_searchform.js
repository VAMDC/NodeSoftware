function validate_required(field,alerttxt)
{

with (field) {
	if (value==null||value=="") {
		alert(alerttxt);return false;
	}
	return true;
}
}

function validate_output_formats()
{
	/*alert('No output format has been specified');*/
	return true;
}

function validate_form(thisform)
{
	with (thisform) {
		/*if (!validate_required(filestem,"You must give your output files a filestem!")) {
			filestem.focus();
			return false;
		}
		if (!validate_nurange()) {
			return false;
		}
		if (!validate_Smin()) {
			return false;
		}*/
		if (!validate_output_formats()) {
			return false;
		}
		/*if (!validate_molecules()) {
			return false;
		}*/
	}
	return true;
}

function xmlhttpPost(strURL) {
	var form = document.forms['SearchForm'];
	if (!validate_form(form)) {
		return false;
	}

	var xmlHttpReq = false;
	var self = this;
	// Mozilla/Safari
	if (window.XMLHttpRequest) {
		self.xmlHttpReq = new XMLHttpRequest();
	}
	// IE 5.x and 6.x
	else if (window.ActiveXObject) {
		self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
	}
	self.xmlHttpReq.open('POST', strURL, true);
	self.xmlHttpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	/*self.xmlHttpReq.onreadystatechange = function() {
		if (self.xmlHttpReq.readyState == 3) {
			updatepage(self.xmlHttpReq.responseText);
		}
	}*/
	qstr=getquerystring(form);
	self.xmlHttpReq.send(qstr);
}

function getquerystring(form) {
	var opts = [];
	var elements=['numin','numax','Smin']
	for (i in form.elements) {
		element = form.elements[i];
		if (elements.indexOf(element.name)>=0) {
			opts.push(escape(element.name) + '=' + escape(element.value));
		}
	}

	qstr=opts.join('&');
	//alert(qstr);
	return qstr;
}

function updatepage(str){
	div_obj = document.getElementById("result")
	div_obj.innerHTML = str;
	<!-- make sure that the latest output is visible by scrolling to the bottom of the div -->
	div_obj.scrollTop = div_obj.scrollHeight;
}

