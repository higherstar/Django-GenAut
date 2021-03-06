# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonSync',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.CharField(max_length=1, choices=[(b'u', b'From GenAut to Amazon'), (b'd', b'From Amazon to GenAut')])),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=50)),
                ('products_total', models.PositiveIntegerField()),
                ('products_synced', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
