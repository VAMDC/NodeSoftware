from django.contrib import admin
from models import *

def keywords(obj):
    return ', '.join([o.name for o in obj.keyword_set.iterator()])

class KeyWordAdmin(admin.ModelAdmin):
    list_display = ('name', 'sdescr')
    search_fields = ('name', 'sdescr', 'ldescr', 'unit')

class UsageAdmin(admin.ModelAdmin):
    list_display = ('name',keywords)

admin.site.register(KeyWord,KeyWordAdmin)
admin.site.register(Usage,UsageAdmin)

