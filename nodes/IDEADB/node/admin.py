from django.contrib import admin

#import your models here like this:
from IDEADB.node.models import *

# add your models here to have them in the admin interface
# for example if you have a model class called "Transition":
admin.site.register(Species)
admin.site.register(Resonance)
admin.site.register(Source)
admin.site.register(Massspec)
admin.site.register(Energyscan)
admin.site.register(Author)
admin.site.register(Experiment)
