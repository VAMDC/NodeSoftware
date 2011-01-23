# Create your views here.
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ValidationError



def validate_dict(data):
#    try eval(data):
    raise ValidationError('bla')
    raise ValidationError('bla2')

class CheckForm(forms.Form):
    content=forms.CharField(label='Paste your dictionary',widget=forms.widgets.Textarea(attrs={'cols':'50','rows':'10'}),required=True,validators=[validate_dict])

def check(request):
    if request.method == 'POST':
        form = CheckForm(request.POST) 
        if form.is_valid():
            #print form.cleaned_data
            pass

    else:
        form=CheckForm()
        
    return render_to_response('dictionary/check.html', RequestContext(request,{'form': form}))
