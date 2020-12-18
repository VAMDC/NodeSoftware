from django.contrib import admin

#import your models here like this:
#from DjNodeExample.node.models import *

from models import *


# add your models here to have them in the admin interface
# for example if you have a model class called "Transition":

class VamdcNodesAdmin(admin.ModelAdmin):
    def make_active(modeladmin, request, queryset):
      queryset.update(status=RecordStatus.ACTIVE)
    make_active.short_description = "Activate selected nodes"
      
    
    def make_disabled(modeladmin, request, queryset):
      queryset.update(status=RecordStatus.DISABLED)
    make_disabled.short_description = "Disable selected nodes"
    
    list_display = ('short_name','status','contact_email','last_update_date')
    
    actions = [make_active,make_disabled]


class VamdcSpeciesAdmin(admin.ModelAdmin):
  def make_verified(modeladmin, request, queryset):
    queryset.update(status=RecordStatus.ACTIVE)
  make_verified.short_description = "Mark as verified"
  
  def make_disabled(modeladmin, request, queryset):
    queryset.update(status=RecordStatus.DISABLED)
  make_disabled.short_description = "Mark as hidden/disabled"
  

  list_display = ('mass_number','stoichiometric_formula', 'structural_formula_all','charge','origin_member_database','status','species_foreign_ids')
    
  actions = [make_verified,make_disabled]
  
class VamdcSpeciesNamesAdmin(admin.ModelAdmin):
  def make_verified(modeladmin, request, queryset):
    queryset.update(status=RecordStatus.ACTIVE)
  make_verified.short_description = "Mark as verified"
  
  def make_disabled(modeladmin, request, queryset):
    queryset.update(status=RecordStatus.DISABLED)
  make_disabled.short_description = "Mark as hidden/disabled"
  

  list_display = ('species','name','id', 'species','status')
    
  actions = [make_verified,make_disabled]


admin.site.register(VamdcNodes,VamdcNodesAdmin)
admin.site.register(VamdcSpecies,VamdcSpeciesAdmin)
#~ admin.site.register(VamdcSpeciesNames,VamdcSpeciesNamesAdmin)
