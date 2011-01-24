# Create your views here.
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ValidationError

from models import *
RETURNA=Usage.objects.get(pk=2)
REQUESTA=Usage.objects.get(pk=3)
RESTRICTA=Usage.objects.get(pk=1)

import re
REGEX1=re.compile(r"""^\s*(RETURNABLE|RESTRICTABLE)\s*=\s*\{(['"]\w+['"]\s*:\s*['"][a-zA-Z0-9_\.]*['"]\s*,?\s*)*\s*\}\s*$""")

REGEX2=re.compile(r"""^(AtomState|Sources|MoleStates|CollTrans|RadTran|Methods|MoleQNs)\.[a-zA-Z0-9_\.]*$""")

from string import strip

def check_keywords(data,usage):
    errors=[]
    for name in data.keys():
        try: r = KeyWord.objects.get(name=name)
        except KeyWord.DoesNotExist:
            errors.append('Keyword %s does not exist in the dictionary.'%name)
            continue
        if not usage in r.usage.all():
            errors.append('%s is not a %s according to the dictionary.'%(name,usage.name))
    if errors: return errors
    else: return None

def check_returnvalues(data):
    errors=[]
    for name in data.keys():
        if not REGEX2.match(data[name]):
            errors.append('The value "%s" of %s does not start with one of the known prefixes. This is fine, if you intend to return as a constant string.'%(data[name],name))
    if errors: return errors
    else: return None
   
def validate_dict(data):
    errors=[]
    if not REGEX1.match(data):
        errors.append('First syntax check did not pass. Please check.')

    name,value = data.split('=')
    name=strip(name)
    value = ''.join(map(strip,value.splitlines()))
    try: value=eval(value)
    except: errors.append('Second check (evalution) did not pass. Please check that your imput is correct Python code.')

    if name == 'RETURNABLE':
        err = check_keywords(value,RETURNA)
        if err: errors += err
        err = check_returnvalues(value)
        if err: errors += err
    elif name == 'RESTRICTABLE':
        err = check_keywords(value,RESTRICTA)
        if err: errors += err
    
    if errors: raise ValidationError(errors)
    
class CheckForm(forms.Form):
    content=forms.CharField(label='Paste your dictionary',
	widget=forms.widgets.Textarea(attrs={'cols':'70','rows':'20'}),
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
