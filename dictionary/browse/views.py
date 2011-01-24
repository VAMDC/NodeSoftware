# Create your views here.
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ValidationError


import re
REGEX1=re.compile(r"""^(RETURNABLE|RESTRICTABLE)\s*=\s*\{(['"]\w*['"]\s*:\s*['"][a-zA-Z0-9_\.]*['"]\s*,\s*)*\s*\}\s*$""")


def check_returnable(ret):
    pass

def check_restrictable(ret):
    pass



def validate_dict(data):
    errors=[]
    if not REGEX1.match(data):
        errors.append('Basic form not met.')

    if errors: raise ValidationError(errors)
    
class CheckForm(forms.Form):
    content=forms.CharField(label='Paste your dictionary',
	widget=forms.widgets.Textarea(attrs={'cols':'50','rows':'10'}),
	required=True,validators=[validate_dict])

def check(request):
    if request.method == 'POST':
        form = CheckForm(request.POST) 
        if form.is_valid():
            #print form.cleaned_data
            pass

    else:
        form=CheckForm()
        
    return render_to_response('dictionary/check.html', RequestContext(request,{'form': form}))
