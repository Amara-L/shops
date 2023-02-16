# Generated by Django 4.1.7 on 2023-02-15 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tutorials.city')),
            ],
        ),
        migrations.CreateModel(
            name='Shops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('open_time', models.IntegerField()),
                ('close_time', models.IntegerField()),
                ('adress_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tutorials.adress')),
            ],
        ),
        migrations.AddField(
            model_name='adress',
            name='street_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tutorials.street'),
        ),
    ]
