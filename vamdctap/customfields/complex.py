"""
LICENSE as of https://bitbucket.org/mp/django-composite-field/
for base.py and complex.py which are taken from there:

Copyright (c) 2010, Michael P. Jung
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of the company nor the names of its contributors may be
       used to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from . import CompositeField
from django.db.models import FloatField


class ComplexField(CompositeField):

    real = FloatField()
    imag = FloatField()

    def __init__(self, verbose_name=None, blank=False, null=False, default=None):
        super(ComplexField, self).__init__()
        self.verbose_name = verbose_name
        for field in (self['real'], self['imag']):
            field.blank = blank
            field.null = blank
        if default is not None:
            self['real'].default = default.real
            self['imag'].default = default.imag

    def contribute_to_class(self, cls, field_name):
        if self.verbose_name is None:
            self.verbose_name = field_name.replace('_', ' ')
        self['real'].verbose_name = 'Re(%s)' % self.verbose_name
        self['imag'].verbose_name = 'Im(%s)' % self.verbose_name
        super(ComplexField, self).contribute_to_class(cls, field_name)

    def get(self, model):
        proxy = self.get_proxy(model)
        real, imag = proxy.real, proxy.imag
        if real is None and imag is None:
            return None
        return complex(real or 0, imag or 0)

    def set(self, model, value):
        proxy = self.get_proxy(model)
        if value is None:
            proxy.real = None
            proxy.imag = None
        else:
            proxy.real = value.real
            proxy.imag = value.imag
