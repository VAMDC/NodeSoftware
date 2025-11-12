# Generated manually for molecular quantum numbers

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_molec', '0001_initial'),
    ]

    operations = [
        # Remove atomic-only quantum number fields
        migrations.RemoveField(
            model_name='state',
            name='l',
        ),
        migrations.RemoveField(
            model_name='state',
            name='j1',
        ),
        migrations.RemoveField(
            model_name='state',
            name='j2',
        ),
        migrations.RemoveField(
            model_name='state',
            name='k',
        ),
        migrations.RemoveField(
            model_name='state',
            name='s2',
        ),
        migrations.RemoveField(
            model_name='state',
            name='jc',
        ),
        migrations.RemoveField(
            model_name='state',
            name='sn',
        ),
        # Add molecular quantum number fields
        migrations.AddField(
            model_name='state',
            name='v',
            field=models.PositiveSmallIntegerField(db_column='v', null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='Lambda',
            field=models.PositiveSmallIntegerField(db_column='Lambda', null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='Sigma',
            field=models.DecimalField(db_column='Sigma', decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='Omega',
            field=models.DecimalField(db_column='Omega', decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='rotN',
            field=models.PositiveSmallIntegerField(db_column='rotN', null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='elecstate',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
