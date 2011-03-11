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
REGEX1=re.compile(r"""^\s*(RETURNABLES|RESTRICTABLES)\s*=\s*\{\s*\\?\s*(['"]\w+['"]\s*:\s*[ru]?['"][\w\-\\_\.,/()\[\]'"=\ ]*['"]\s*,?\s*)*\s*\}\s*$""")

REGEX2=re.compile(r"""^(Atom|AtomState|Source|Molecule|MoleculeState|CollTran|RadTran|Method|MoleQNs)\..*$""")

from string import strip,lower

def browse_by_type(request):
    atoms = KeyWord.objects.filter(block__in=('at','as'))
    atoms.desc = 'Atoms and atomic states'
    atoms.tag = 'at'
    molecs = KeyWord.objects.filter(block__in=('mo','ms','mq'))
    molecs.desc = 'Molecules, their states and quantum numbers'
    molecs.tag = 'mo'
    noxsams = KeyWord.objects.filter(block=None)
    noxsams.desc = 'Keywords without a place in XSAMS'
    noxsams.tag = 'nx'
    procs = KeyWord.objects.filter(block__in=('rt','ct','nr'))
    procs.desc = 'Processes'
    procs.tag = 'pr'
    oth = KeyWord.objects.filter(block__in=('en','fu','me','so'))
    oth.desc = 'Environments, Functions, Methods and Sources'
    oth.tag = 'oh'
    blocs = [atoms, molecs, procs, oth, noxsams]
    return render_to_response('dictionary/bytype.html',
        RequestContext(request,{'blocs': blocs}))

def bareKW(kw):
    kw = kw.lower()
    suffixes=['unit','ref','comment','accuracy','method']
    for suff in suffixes:
        if kw.endswith(suff):
            return kw.rsplit(suff,1)[0]

def check_keyword_exists(kw):
    try: KeyWord.objects.get(name__iexact=kw)
    except KeyWord.DoesNotExist:
        barekw = bareKW(kw)
        if not barekw:
            return 'Keyword %s does not exist in the dictionary.'%kw

        try: k = KeyWord.objects.get(name__iexact=barekw)
        except KeyWord.DoesNotExist:
            return 'Keyword %s does not exist in the dictionary. (It is used with one of the DataType suffixes)'%barekw
        if not k.datatype:
            return 'Your used keyword %s with a DataType suffix but it is not a DataType.'%barekw

def check_keyword_usage(kw,usage):
    try: kw = KeyWord.objects.get(name__iexact=kw)
    except: return
    if not usage in kw.usage.all():
        return '%s is not a %s according to the dictionary.'%(kw,usage.name)

def check_returnvalues(kw,value):
    if not REGEX2.match(value):
        return 'The value "%s" of %s does not start with one of the known prefixes. This is fine, if you intend to return this as a constant string.'%(value,kw)

def check_unit(kw,keys):
    try: k = KeyWord.objects.get(name__iexact=kw)
    except: return
    if k.datatype:
        keys = map(lower,keys)
        if not kw.lower() + 'unit' in keys:
            return 'You use the DataType %s but not the corresponding keyword for its unit (%sUnit).'%(kw,kw)

def validate_dict(data):
    errors=[]
    if not REGEX1.match(data):
        errors.append('First syntax check did not pass. (Comments with # are not allowed in this check.)')

    name,value = data.split('=')
    name=strip(name)
    if name == 'RETURNABLES': usage = RETURNA
    elif name == 'RESTRICTABLES': usage = RESTRICTA
    else: errors.append('Neither RETURNABLES or RESTRICTABLES assignment found')
    value = ''.join(map(strip,map(strip,value.splitlines()),'\\'))
    try: value=eval(value)
    except:
        errors.append('Second check (evalution) did not pass. Please check that your input is correct Python code.')
        raise ValidationError(errors)

    for kw in value.keys():
        err = check_keyword_exists(kw)
        if err:
            errors.append(err)
            continue
        err = check_keyword_usage(kw,usage)
        if err: errors.append(err)
        if usage==RETURNA:
            err = check_returnvalues(kw,value[kw])
            if err: errors.append(err)
            err = check_unit(kw,value.keys())
            if err: errors.append(err)
    if errors: raise ValidationError(errors)

class CheckForm(forms.Form):
    content=forms.CharField(label='Paste your dictionary',
    widget=forms.widgets.Textarea(attrs={'cols':'80','rows':'25'}),
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
'as':'AtomState.',
'ms':'MoleculeState.',
'mq':'MoleQNs.',
'ct':'CollTran.',
'rt':'RadTran.',
'me':'Method.',
'mo':'Molecule.',
'at':'AtomState.',
}

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
