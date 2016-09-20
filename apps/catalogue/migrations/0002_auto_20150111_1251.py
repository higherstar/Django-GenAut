# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVehicleCompatibility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.ForeignKey(related_name='compatibilities', to='catalogue.Product')),
            ],
            options={
                'verbose_name': 'Product Vehicle Compatibility',
                'verbose_name_plural': 'Product Vehicle Compatibilities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vehicle', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Vehicle',
                'verbose_name_plural': 'Vehicles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VehicleBrand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vehicle_brand', models.CharField(default=b'', max_length=255)),
            ],
            options={
                'verbose_name': 'Vehicle Brand',
                'verbose_name_plural': 'Vehicle Brands',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vehicle_model', models.CharField(max_length=255)),
                ('vehicle', models.ForeignKey(to='catalogue.Vehicle')),
                ('vehicle_brand', models.ForeignKey(related_name='models', to='catalogue.VehicleBrand')),
            ],
            options={
                'verbose_name': 'Vehicle Model',
                'verbose_name_plural': 'Vehicle Models',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vehicle_type', models.CharField(max_length=255)),
                ('vehicle_model', models.ForeignKey(related_name='types', to='catalogue.VehicleModel')),
            ],
            options={
                'ordering': ('vehicle_type',),
                'verbose_name': 'Vehicle Type',
                'verbose_name_plural': 'Vehicle Types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='productvehiclecompatibility',
            name='vehicle_type',
            field=models.ForeignKey(to='catalogue.VehicleType'),
            preserve_default=True,
        ),
    ]
