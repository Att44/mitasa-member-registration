# Generated by Django 5.0.3 on 2024-07-24 01:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_alter_member_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kod', models.CharField(max_length=200, null=True)),
                ('jbtn', models.CharField(max_length=200, null=True)),
                ('keterangan', models.CharField(max_length=200, null=True)),
                ('noPekerja', models.CharField(max_length=200, null=True)),
                ('nama', models.CharField(max_length=200, null=True)),
                ('noIC', models.CharField(max_length=200, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('date', models.DateField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='member.member')),
            ],
        ),
    ]
