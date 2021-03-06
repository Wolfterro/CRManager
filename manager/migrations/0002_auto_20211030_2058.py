# Generated by Django 3.2.8 on 2021-10-30 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20211030_2058'),
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name': 'Atividade', 'verbose_name_plural': 'Atividades'},
        ),
        migrations.AlterModelOptions(
            name='cr',
            options={'verbose_name': 'CR', 'verbose_name_plural': 'CRs'},
        ),
        migrations.AlterModelOptions(
            name='process',
            options={'verbose_name': 'Processo', 'verbose_name_plural': 'Processos'},
        ),
        migrations.AddField(
            model_name='process',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='Usuário'),
        ),
    ]
