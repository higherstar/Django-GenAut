# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20150203_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='OriginalProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_order', models.PositiveIntegerField(default=0)),
                ('url', models.URLField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(related_name='original_images', to='catalogue.Product')),
            ],
            options={
                'ordering': ['display_order'],
                'verbose_name': 'Product original image',
                'verbose_name_plural': 'Product original images',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='originalproductimage',
            unique_together=set([('product', 'display_order')]),
        ),
    ]
