# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Author.lastname'
        db.alter_column('node_author', 'lastname', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Author.firstname'
        db.alter_column('node_author', 'firstname', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Author.email'
        db.alter_column('node_author', 'email', self.gf('django.db.models.fields.EmailField')(max_length=254))
        # Adding field 'Species.chemical_formula'
        db.add_column(u'species', 'chemical_formula',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40, db_index=True),
                      keep_default=False)


        # Changing field 'Species.name'
        db.alter_column(u'species', 'name', self.gf('django.db.models.fields.CharField')(max_length=40))

    def backwards(self, orm):

        # Changing field 'Author.lastname'
        db.alter_column('node_author', 'lastname', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'Author.firstname'
        db.alter_column('node_author', 'firstname', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'Author.email'
        db.alter_column('node_author', 'email', self.gf('django.db.models.fields.TextField')())
        # Deleting field 'Species.chemical_formula'
        db.delete_column(u'species', 'chemical_formula')


        # Changing field 'Species.name'
        db.alter_column(u'species', 'name', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        'node.author': {
            'Meta': {'object_name': 'Author'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'pageend': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'pagestart': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'journal'", 'max_length': '17'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'node.species': {
            'Meta': {'object_name': 'Species', 'db_table': "u'species'"},
            'chemical_formula': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inchi': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'mass': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'molecule': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '40', 'blank': 'True'}),
            'nuclear_charge': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '3'})
        }
    }

    complete_apps = ['node']