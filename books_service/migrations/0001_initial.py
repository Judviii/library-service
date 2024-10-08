# Generated by Django 4.0.4 on 2024-08-13 00:15

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('author', models.CharField(max_length=64)),
                ('cover', models.CharField(choices=[('SOFT', 'Soft'), ('HARD', 'Hard')], default='SOFT', max_length=4)),
                ('inventory', models.PositiveIntegerField()),
                ('daily_fee', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Daily fee (in $USD)')),
            ],
            options={
                'ordering': ['title'],
                'unique_together': {('title', 'author', 'cover')},
            },
        ),
    ]
