# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_auto_20150204_1039'),
        ('ebay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductEbayId',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ebay_id', models.CharField(max_length=63)),
                ('product', models.OneToOneField(related_name='ebay_id', to='catalogue.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
