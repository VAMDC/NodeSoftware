from django.contrib import admin
from django.contrib.admin.models import LogEntry
from models import *

RETURNA=Usage.objects.get(pk=2)
REQUESTA=Usage.objects.get(pk=3)
RESTRICTA=Usage.objects.get(pk=1)

def log_usagechange(use,addORrem):
    logentr = LogEntry(user=request.user)

def keywords(obj):
    return ', '.join([o.name for o in obj.keyword_set.iterator()])

def make_returnable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.add(RETURNA)
#    LogEntry.objects.log_action( user=request.user,
#				change_message='')
make_returnable.short_description = "Mark selected keywords Returnable"

def unmake_returnable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.remove(RETURNA)
unmake_returnable.short_description = "Unmark selected keywords Returnable"

def make_requestable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.add(REQUESTA)
make_requestable.short_description = "Mark selected keywords Requestable"

def unmake_requestable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.remove(REQUESTA)
unmake_requestable.short_description = "Unmark selected keywords Requestable"

def make_restrictable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.add(RESTRICTA)
make_restrictable.short_description = "Mark selected keywords Restrictable"

def unmake_restrictable(modeladmin, request, queryset):
    for kw in queryset: kw.usage.remove(RESTRICTA)
unmake_restrictable.short_description = "Unmark selected keywords Restrictable"

def toggle_datatype(modeladmin, request, queryset):
    for kw in queryset:
        kw.datatype = not kw.datatype
        kw.save()
toggle_datatype.short_description = "Toggle DataType true/false for selected keywords"

class KeyWordAdmin(admin.ModelAdmin):
    list_display = ('name', 'sdescr','datatype','unit')
    search_fields = ('name', 'sdescr', 'ldescr', 'unit')
    actions_on_top = True
    actions_on_bottom = True
    actions = [toggle_datatype,make_returnable,unmake_returnable,unmake_requestable,make_requestable, make_restrictable, unmake_restrictable]

class UsageAdmin(admin.ModelAdmin):
    list_display = ('name',keywords)

admin.site.register(KeyWord,KeyWordAdmin)
admin.site.register(Usage,UsageAdmin)

