# Generated by Django 3.0.5 on 2020-04-19 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tcmanage', '0006_auto_20200419_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tccase',
            name='tc_module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='module', to='tcmanage.TcModule'),
        ),
    ]