from django.contrib import admin

#import your models here like this:
from IDEADB.node.models import *

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('chemical_formula', 'name', 'mass')
    search_fields = ('chemical_formula', 'name', 'mass')

class SourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'journal', 'year')
    search_fields = ('title', 'journal', 'year')
    filter_horizontal = ('authors',)

class EnergyscanAdmin(admin.ModelAdmin):
    list_display = ('species', 'origin_species')
    search_fields = ('species', 'origin_species')
    raw_id_fields = ('species', 'origin_species')

admin.site.register(Species, SpeciesAdmin)
admin.site.register(Resonance)
admin.site.register(Source, SourceAdmin)
admin.site.register(Massspec)
admin.site.register(Energyscan, EnergyscanAdmin)
admin.site.register(Author)
admin.site.register(Experiment)
