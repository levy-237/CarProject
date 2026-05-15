# Generated manually for EV listing details.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0017_listing_battery_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="factory_range",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="listing",
            name="real_summer_range",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="listing",
            name="real_winter_range",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="listing",
            name="garantie",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="listing",
            name="pickerl",
            field=models.BooleanField(default=False),
        ),
    ]
