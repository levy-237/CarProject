# Generated manually for EV charging specs.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0005_cardrivetrain"),
    ]

    operations = [
        migrations.AddField(
            model_name="carmodeltrim",
            name="max_ac_charge_kw",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="carmodeltrim",
            name="max_dc_charge_kw",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="carmodeltrim",
            name="twenty_to_eighty_charge_min",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
