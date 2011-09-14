from django.db import models
#from django.core.exceptions import ValidationError
#
#class Conversion(models.Model):
#    datetime = models.DateTimeField(auto_now_add=True)
#    infile = models.FileField(upload_to='%x-%X',verbose_name='Input file',null=True, blank=True)
#    inurl = models.URLField(verify_exists=False, max_length=1024, verbose_name='Input URL',null=True, blank=True)
#
#    def clean(self):
#        if (not (self.infile or self.inurl)) \
#            or (self.infile and self.inurl):
#            raise ValidationError('Give either input file or URL')
