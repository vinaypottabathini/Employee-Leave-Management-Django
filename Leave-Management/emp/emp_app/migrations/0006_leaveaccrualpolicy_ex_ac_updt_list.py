# Generated by Django 2.2 on 2021-06-06 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp_app', '0005_leaveaccrualpolicy_ac_ndays_incre_decre'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveaccrualpolicy',
            name='ex_ac_updt_list',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
