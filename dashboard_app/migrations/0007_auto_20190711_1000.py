# Generated by Django 2.2 on 2019-07-11 05:00

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0006_auto_20190710_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='position2',
            field=smart_selects.db_fields.GroupedForeignKey(blank=True, group_field='s_subject', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='m2', to='dashboard_app.Student_Enroll'),
        ),
        migrations.AlterField(
            model_name='team',
            name='position3',
            field=smart_selects.db_fields.GroupedForeignKey(blank=True, group_field='s_subject', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='m3', to='dashboard_app.Student_Enroll'),
        ),
    ]
