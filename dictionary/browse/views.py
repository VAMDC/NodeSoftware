# Create your views here.
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms.models import modelformset_factory
#from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, HttpResponse

from models import Usage,KeyWord
RETURNA=Usage.objects.get(pk=2)
REQUESTA=Usage.objects.get(pk=3)
RESTRICTA=Usage.objects.get(pk=1)

import re
REGEX1=re.compile(r"""^\s*(RETURNABLES|RESTRICTABLES)\s*=\s*\{\s*\\?\s*(['"]\w+['"]\s*:\s*['"][a-zA-Z0-9_\.]*['"]\s*,?\s*)*\s*\}\s*$""")

REGEX2=re.compile(r"""^(AtomState|Source|MoleState|CollTran|RadTran|Method|MoleQNs)\.[a-zA-Z0-9_\.]*$""")

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
            errors.append('The value "%s" of %s does not start with one of the known prefixes. This is fine, if you intend to return it as a constant string.'%(data[name],name))
    if errors: return errors
    else: return None
   
def validate_dict(data):
    errors=[]
    if not REGEX1.match(data):
        errors.append('First syntax check did not pass. Please check.')

    name,value = data.split('=')
    name=strip(name)
    value = ''.join(map(strip,map(strip,value.splitlines()),'\\'))
    try: value=eval(value)
    except:
        errors.append('Second check (evalution) did not pass. Please check that your input is correct Python code.')
        raise ValidationError(errors)

    if name == 'RETURNABLES':
        err = check_keywords(value,RETURNA)
        if err: errors += err
        err = check_returnvalues(value)
        if err: errors += err
    elif name == 'RESTRICTABLES':
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


#########
blockmap = {'so':'Source.',
'as':'AtomicState.',
'ms':'MoleState.',
'mq':'MoleQNs.',
'ct':'CollTran.',
'rt':'RadTran.',
'me':'Method.',
'mo':'Molecule.',
'at':'AtomState.',
'sp':'Specie.'}

def makedicts(selected):
    content = 'RETURNABLES = {\ \n'
    for kw in selected:
        if RETURNA in kw.usage.iterator():
            if blockmap.has_key(kw.block): prefix=blockmap[kw.block]
            else: prefix=''
            content += '\'%s\':\'%s\',\n'%(kw.name,prefix)

    content += '}\n\n\n'
    content += 'RESTRICTABLES = {\ \n'
    for kw in selected:
        if RESTRICTA in kw.usage.iterator():
            content += '\'%s\':\'\',\n'%kw.name

    content += '}\n\n\n'
    content += """
# Do not edit or remove these three lines
from vamdctap.caselessdict import CaselessDict
RETURNABLES = CaselessDict(RETURNABLES)
RESTRICTABLES = CaselessDict(RESTRICTABLES)
"""
    return content

class SelectKeyWordFormSet(forms.models.BaseModelFormSet):
    def add_fields(self, form, index):
        super(SelectKeyWordFormSet, self).add_fields(form, index)
        form.fields["include"] = forms.BooleanField(required=False, label="Include this keyword")
    

def makenew(request):
    q = Q(usage=RESTRICTA) | Q(usage=RETURNA)
    queryset = KeyWord.objects.filter(q).distinct()
    MakeNewFormSet = modelformset_factory(KeyWord,formset=SelectKeyWordFormSet,extra=0)
        
    if request.method == 'POST':
        formset = MakeNewFormSet(request.POST,request.FILES,queryset=queryset)
        if formset.is_valid():
            selected=[]
            for form in formset.cleaned_data:
                if form['include']: selected.append(form['id'])

            filecontent = makedicts(selected)
            response=HttpResponse(filecontent,mimetype='text/x-python')
            response['Content-Disposition'] = 'attachment; filename=dictionaries.py'
            return response

    else:
        formset = MakeNewFormSet(queryset=queryset)

    return render_to_response('dictionary/makenew.html', RequestContext(request,{'formset': formset}))
