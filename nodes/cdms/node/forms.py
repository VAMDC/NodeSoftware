from models import *
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from django.forms.models import modelformset_factory
from cdmsportalfunc import *
from django.core.exceptions import ValidationError

class MoleculeForm(ModelForm):
    class Meta:
        model = Molecules

class SpecieForm(ModelForm):
    datearchived  = forms.DateField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
        )

    dateactivated = forms.DateField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
        )

    
    class Meta:
        model = Species

class FilterForm(ModelForm):
    class Meta:
        model = QuantumNumbersFilter


class XsamsConversionForm(forms.Form):

    inurl = forms.URLField(label='Input URL',required=False, widget=forms.TextInput(attrs={'size': 50, 'title': 'Paste here a URL that delivers an XSAMS document.',}))
    #inurl = forms.CharField(max_length=50)
    infile  = forms.FileField()
    format = forms.ChoiceField( choices = [("RAD 3D", "RAD 3D"),("CSV","CSV")],
                               )
    def clean(self):
        infile = self.cleaned_data.get('infile')
        inurl = self.cleaned_data.get('inurl')
        if (infile and inurl):
            raise ValidationError('Give either input file or URL!')

        if inurl:
            try: data = urlopen(inurl)
            except Exception,err:
                raise ValidationError('Could not open given URL: %s'%err)
        elif infile: data = infile
        else:
            raise ValidationError('Give either input file or URL!')

        try: self.cleaned_data['result'] = applyStylesheet2File(data)
        except Exception,err:
            raise ValidationError('Could not transform XML file: %s'%err)

#        try: xml=e.parse(data)
#        except Exception,err:
#            raise ValidationError('Could not parse XML file: %s'%err)
#        try: self.cleaned_data['sme'] = xsl(xml)
#        except Exception,err:
#            raise ValidationError('Could not transform XML file: %s'%err)

        return self.cleaned_data
