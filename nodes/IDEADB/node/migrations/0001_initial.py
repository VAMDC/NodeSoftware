# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table('node_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('email', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('node', ['Author'])

        # Adding model 'Experiment'
        db.create_table('node_experiment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('node', ['Experiment'])

        # Adding model 'Species'
        db.create_table(u'species', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('mass', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('nuclear_charge', self.gf('django.db.models.fields.SmallIntegerField')(max_length=3)),
            ('inchi', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('molecule', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('node', ['Species'])

        # Adding model 'Source'
        db.create_table('node_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('doi', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('pagestart', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('pageend', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('type', self.gf('django.db.models.fields.CharField')(default='journal', max_length=17)),
        ))
        db.send_create_signal('node', ['Source'])

        # Adding M2M table for field authors on 'Source'
        db.create_table('node_source_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('source', models.ForeignKey(orm['node.source'], null=False)),
            ('author', models.ForeignKey(orm['node.author'], null=False))
        ))
        db.create_unique('node_source_authors', ['source_id', 'author_id'])

        # Adding model 'Energyscan'
        db.create_table('node_energyscan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(related_name='energyscan_species', to=orm['node.Species'])),
            ('origin_species', self.gf('django.db.models.fields.related.ForeignKey')(related_name='energyscan_origin_species', to=orm['node.Species'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['node.Source'])),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['node.Experiment'])),
            ('energyscan_data', self.gf('django.db.models.fields.TextField')()),
            ('productiondate', self.gf('django.db.models.fields.DateField')()),
            ('energyresolution', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
        ))
        db.send_create_signal('node', ['Energyscan'])

        # Adding model 'Resonance'
        db.create_table('node_resonance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('energyscan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['node.Energyscan'])),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resonance_species', to=orm['node.Species'])),
            ('origin_species', self.gf('django.db.models.fields.related.ForeignKey')(related_name='resonance_origin_species', to=orm['node.Species'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['node.Source'])),
            ('energy', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('width', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
        ))
        db.send_create_signal('node', ['Resonance'])

        # Adding model 'Massspec'
        db.create_table('node_massspec', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(related_name='massspec_species', to=orm['node.Species'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['node.Source'])),
            ('energy', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('massspec_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('node', ['Massspec'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table('node_author')

        # Deleting model 'Experiment'
        db.delete_table('node_experiment')

        # Deleting model 'Species'
        db.delete_table(u'species')

        # Deleting model 'Source'
        db.delete_table('node_source')

        # Removing M2M table for field authors on 'Source'
        db.delete_table('node_source_authors')

        # Deleting model 'Energyscan'
        db.delete_table('node_energyscan')

        # Deleting model 'Resonance'
        db.delete_table('node_resonance')

        # Deleting model 'Massspec'
        db.delete_table('node_massspec')


    models = {
        'node.author': {
            'Meta': {'object_name': 'Author'},
            'email': ('django.db.models.fields.TextField', [], {}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'node.energyscan': {
            'Meta': {'object_name': 'Energyscan'},
            'energyresolution': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'energyscan_data': ('django.db.models.fields.TextField', [], {}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['node.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin_species': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'energyscan_origin_species'", 'to': "orm['node.Species']"}),
            'productiondate': ('django.db.models.fields.DateField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['node.Source']"}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'energyscan_species'", 'to': "orm['node.Species']"})
        },
        'node.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'node.massspec': {
            'Meta': {'object_name': 'Massspec'},
            'energy': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'massspec_data': ('django.db.models.fields.TextField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['node.Source']"}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'massspec_species'", 'to': "orm['node.Species']"})
        },
        'node.resonance': {
            'Meta': {'object_name': 'Resonance'},
            'energy': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'energyscan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['node.Energyscan']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin_species': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resonance_origin_species'", 'to': "orm['node.Species']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['node.Source']"}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'resonance_species'", 'to': "orm['node.Species']"}),
            'width': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'})
        },
        'node.source': {
            'Meta': {'object_name': 'Source'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['node.Author']", 'symmetrical': 'False'}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'pageend': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'pagestart': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'journal'", 'max_length': '17'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'node.species': {
            'Meta': {'object_name': 'Species', 'db_table': "u'species'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inchi': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'mass': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'molecule': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'nuclear_charge': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['node']