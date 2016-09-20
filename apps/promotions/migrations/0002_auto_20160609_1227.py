# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiHTML',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('raw_htmls', models.ManyToManyField(help_text='Choose the RawHTML content blocks that this block will use. (You may need to create some first).', to='promotions.RawHTML', blank=True)),
            ],
            options={
                'verbose_name': 'Multi HTML',
                'verbose_name_plural': 'Multi HTML',
            },
        ),
        migrations.AlterField(
            model_name='handpickedproductlist',
            name='products',
            field=models.ManyToManyField(to='catalogue.Product', verbose_name='Products', through='promotions.OrderedProduct', blank=True),
        ),
        migrations.AlterField(
            model_name='multiimage',
            name='images',
            field=models.ManyToManyField(help_text='Choose the Image content blocks that this block will use. (You may need to create some first).', to='promotions.Image', blank=True),
        ),
    ]
