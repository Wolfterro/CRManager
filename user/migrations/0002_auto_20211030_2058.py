# Generated by Django 3.2.8 on 2021-10-30 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Endereço', 'verbose_name_plural': 'Endereços'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Perfil de Usuário', 'verbose_name_plural': 'Perfis de Usuários'},
        ),
    ]
