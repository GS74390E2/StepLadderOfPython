# Generated by Django 2.1.7 on 2019-03-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indextypegoodsbanner',
            name='display_type',
            field=models.SmallIntegerField(choices=[(1, '图片'), (0, '标题')], default=1, verbose_name='展示类型'),
        ),
    ]
