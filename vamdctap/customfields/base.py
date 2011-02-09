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

from copy import deepcopy

from django.db.models.fields import Field
from django.utils.datastructures import SortedDict


class CompositeFieldBase(type):
    '''Metaclass for all composite fields.'''

    def __new__(cls, name, bases, attrs):
        super_new = super(CompositeFieldBase, cls).__new__
        # If this isn't a subclass of CompositeField, don't do anything special.
        if not any(isinstance(b, CompositeFieldBase) for b in bases):
            return super_new(cls, name, bases, attrs)

        # Prepare attributes.
        fields = []
        for field_name, field in attrs.items():
            if hasattr(field, 'contribute_to_class'):
                fields.append((field_name, field))
                del attrs[field_name]
        fields.sort(key=lambda x: x[1].creation_counter)
        attrs['subfields'] = SortedDict(fields)

        # Create the class.
        new_class = super_new(cls, name, bases, attrs)
        return new_class


class CompositeField(object):
    __metaclass__ = CompositeFieldBase

    def contribute_to_class(self, cls, field_name):
        self.field_name = field_name
        if self.prefix is None:
            self.prefix = '%s_' % field_name
        for subfield_name, subfield in self.subfields.iteritems():
            name = self.prefix + subfield_name
            if hasattr(cls, name):
                raise RuntimeError('contribute_to_class for %s.%s failed due to ' \
                        'duplicate field name %s' % (cls.__name__, field_name, name))
            subfield.contribute_to_class(cls, name)
        setattr(cls, field_name, property(self.get, self.set))

    def __init__(self, prefix=None):
        self.prefix = prefix
        self.subfields = deepcopy(self.subfields)
        for subfield in self.subfields.itervalues():
            subfield.creation_counter = Field.creation_counter
            Field.creation_counter += 1

    def __getitem__(self, name):
        return self.subfields[name]

    def __setitem__(self, name, subfield):
        self.subfields[name] = subfield

    def __contains__(self, name):
        return name in self.subfields

    def __iter__(self):
        return self.subfields.iterkeys()

    def get_proxy(self, model):
        return CompositeField.Proxy(self, model)

    def get(self, model):
        return self.get_proxy(model)

    def set(self, model, value):
        self.get_proxy(model)._set(value)

    class Proxy(object):

        def __init__(self, composite_field, model):
            object.__setattr__(self, '_composite_field', composite_field)
            object.__setattr__(self, '_model', model)

        def _subfield_name(self, name):
            if not name in self._composite_field:
                raise AttributeError('%r object has no attribute %r' % (
                        self._composite_field.__class__.__name__, name))
            return self._composite_field.prefix + name

        def _set(self, values):
            for name in self._composite_field:
                subfield_name = self._composite_field.prefix + name
                setattr(self._model, subfield_name, getattr(values, name))

        def __setattr__(self, name, value):
            setattr(self._model, self._subfield_name(name), value)

        def __getattr__(self, name):
            return getattr(self._model, self._subfield_name(name))

        def __cmp__(self, another):
            for name in self._composite_field:
                pred = cmp(getattr(self, name),
                         getattr(another, name))
                if pred != 0:
                    return pred
            return 0

        def __repr__(self):
            fields = ', '.join(
                '%s=%r' % (name, getattr(self, name))
                        for name in self._composite_field
            )
            return '%s(%s)' % (self._composite_field.__class__.__name__, fields)
