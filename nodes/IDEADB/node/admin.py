from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib import messages

#import your models here like this:
from IDEADB.node.models import *

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('chemical_formula', 'name', 'mass')
    search_fields = ('chemical_formula', 'name', 'mass')

    actions = ['create_new_species_based_on_existing_one']

    def create_new_species_based_on_existing_one(self, request, queryset):
        if len(queryset) == 1:
            s = queryset.get()
            return HttpResponseRedirect('add/?chemical_formula=%s&mass=%s&nuclear_charge=%s' % (s.chemical_formula, s.mass, s.nuclear_charge))
        else:
            messages.error(request, 'You can only base a new species on one existing species, stupid.')

class SourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'journal', 'year')
    search_fields = ('title', 'journal', 'year', 'authors__lastname', 'authors__firstname')
    filter_horizontal = ('authors',)

class EnergyscanAdmin(admin.ModelAdmin):
    list_display = ('species', 'origin_species')
    search_fields = ('species__chemical_formula', 'species__name', 'origin_species__chemical_formula', 'origin_species__name')
    raw_id_fields = ('species', 'origin_species')

admin.site.register(Species, SpeciesAdmin)
admin.site.register(Resonance)
admin.site.register(Source, SourceAdmin)
admin.site.register(Massspec)
admin.site.register(Energyscan, EnergyscanAdmin)
admin.site.register(Author)
admin.site.register(Experiment)
