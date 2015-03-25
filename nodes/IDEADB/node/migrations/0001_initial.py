# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import IDEADB.node.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('middlename', models.CharField(max_length=30, blank=True)),
                ('email', models.EmailField(max_length=254, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Energyscan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('energyscan_data', models.TextField(verbose_name=b'Paste data from Origin in this field')),
                ('y_units', models.CharField(default=b'1/s', max_length=3, verbose_name=b'Please choose units for y-axis', choices=[(b'1/s', b'1/s'), (b'cm2', b'cm2'), (b'm2', b'm2'), (b'unitless', b'unitless')])),
                ('productiondate', models.DateField(verbose_name=b'Production Date')),
                ('comment', models.TextField(max_length=2000, verbose_name=b'Comment (max. 2000 chars.)', blank=True)),
                ('energyresolution', models.DecimalField(verbose_name=b'Energy Resolution of the Experiment in eV', max_digits=4, decimal_places=3)),
                ('lastmodified', models.DateTimeField(default=datetime.datetime(2015, 3, 25, 15, 47, 17, 984783), auto_now=True, auto_now_add=True)),
                ('numberofpeaks', models.IntegerField(verbose_name=b'Number of peaks visible (no shoulder structures)', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Massspec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('energy', models.DecimalField(max_digits=5, decimal_places=2)),
                ('massspec_data', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resonance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('energy', models.DecimalField(max_digits=5, decimal_places=2)),
                ('width', models.DecimalField(max_digits=3, decimal_places=2)),
                ('energyscan', models.ForeignKey(to='node.Energyscan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('journal', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=4)),
                ('number', models.CharField(max_length=6, blank=True)),
                ('volume', models.CharField(max_length=6)),
                ('doi', models.CharField(max_length=100, verbose_name=b'DOI', blank=True)),
                ('pagestart', models.CharField(max_length=5, verbose_name=b'Starting Page')),
                ('pageend', models.CharField(max_length=5, verbose_name=b'Ending Page')),
                ('url', models.URLField(blank=True)),
                ('title', models.CharField(max_length=500)),
                ('type', models.CharField(default=b'journal', max_length=17, choices=[(b'book', b'Book'), (b'database', b'Database'), (b'journal', b'Journal'), (b'preprint', b'Preprint'), (b'private communication', b'Private Communication'), (b'proceeding', b'Proceeding'), (b'report', b'Report'), (b'thesis', b'Thesis'), (b'vamdc node', b'VAMDC Node')])),
                ('authors', models.ManyToManyField(to='node.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(blank=True, max_length=100, verbose_name=b'Common Name (e.g. Water for H2O)', db_index=True, validators=[IDEADB.node.models.validate_name])),
                ('chemical_formula', models.CharField(default=b'', max_length=40, verbose_name=b'Chemical Formula', db_index=True, validators=[IDEADB.node.models.validate_chemical_formula])),
                ('mass', models.PositiveIntegerField(verbose_name=b'Nominal Mass', db_index=True)),
                ('isotope', models.BooleanField(default=True, verbose_name=b'Tick, if this is the most abundant isotope')),
                ('nuclear_charge', models.PositiveSmallIntegerField(max_length=3, null=True, verbose_name=b'Number of Protons', blank=True)),
                ('inchi', models.CharField(db_index=True, max_length=300, verbose_name=b'InChI', blank=True)),
                ('inchikey', models.CharField(db_index=True, max_length=27, verbose_name=b'InChI-Key', blank=True)),
                ('cas', models.CharField(blank=True, max_length=12, verbose_name=b'CAS-Number', validators=[IDEADB.node.models.validate_CAS])),
                ('molecule', models.BooleanField(verbose_name=b'Tick, if this is a molecule')),
            ],
            options={
                'ordering': ['chemical_formula', 'name'],
                'db_table': 'species',
                'verbose_name_plural': 'Species',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resonance',
            name='origin_species',
            field=models.ForeignKey(related_name='resonance_origin_species', to='node.Species'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resonance',
            name='source',
            field=models.ForeignKey(to='node.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resonance',
            name='species',
            field=models.ForeignKey(related_name='resonance_species', to='node.Species'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massspec',
            name='source',
            field=models.ForeignKey(to='node.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='massspec',
            name='species',
            field=models.ForeignKey(related_name='massspec_species', to='node.Species'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='energyscan',
            name='experiment',
            field=models.ForeignKey(to='node.Experiment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='energyscan',
            name='origin_species',
            field=models.ForeignKey(related_name='energyscan_origin_species', to='node.Species'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='energyscan',
            name='source',
            field=models.ForeignKey(to='node.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='energyscan',
            name='species',
            field=models.ForeignKey(related_name='energyscan_species', to='node.Species'),
            preserve_default=True,
        ),
    ]
