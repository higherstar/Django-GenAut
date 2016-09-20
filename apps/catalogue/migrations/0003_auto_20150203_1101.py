# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20150111_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDeliveryOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_available', models.BooleanField(default=True)),
                ('fast_dispatch', models.BooleanField(default=False)),
                ('delivery_time', models.BooleanField(default=False)),
                ('special_order', models.BooleanField(default=False)),
                ('product', models.OneToOneField(related_name='delivery_options', to='catalogue.Product')),
            ],
            options={
                'verbose_name': 'Product Delivery Options',
                'verbose_name_plural': 'Products Delivery Options',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='vehicletype',
            options={'ordering': ('vehicle_model__vehicle_brand__vehicle_brand', 'vehicle_model__vehicle_model', 'vehicle_type'), 'verbose_name': 'Vehicle Type', 'verbose_name_plural': 'Vehicle Types'},
        ),
    ]
