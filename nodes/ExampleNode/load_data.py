#!/usr/bin/env python
"""
Load the example data (the files *.sqlite3.txt) into the database.

    $ python load_data.py

The data go through the Django models, so this works with any database
engine. Existing rows in the four tables are deleted first.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

def load(model, fname, recordsep='\n'):
    """
    Fill one table from a file with one record per line (or per recordsep),
    fields separated by semicolons in the order of the model's fields.
    """
    fields = [f.attname for f in model._meta.concrete_fields]
    with open(os.path.join(HERE, fname)) as f:
        records = [r for r in f.read().split(recordsep) if r.strip()]
    objs = []
    for record in records:
        # the last field may itself contain semicolons (BibTeX)
        values = [v.strip() for v in record.split(';', len(fields)-1)]
        values = [None if v == 'NULL' else v for v in values]
        objs.append(model(**dict(zip(fields, values))))
    model.objects.bulk_create(objs)
    return len(objs)

def load_all():
    from node import models
    for model in (models.Transition, models.State, models.Species, models.Reference):
        model.objects.all().delete()
    return {
        # BibTeX entries span several lines, so these records end with |
        'refs': load(models.Reference, 'references.sqlite3.txt', recordsep='|'),
        'species': load(models.Species, 'species.sqlite3.txt'),
        'states': load(models.State, 'states.sqlite3.txt'),
        'transitions': load(models.Transition, 'transitions.sqlite3.txt'),
        }

if __name__ == "__main__":
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    django.setup()
    for table, n in load_all().items():
        print('%s: %d rows' % (table, n))
