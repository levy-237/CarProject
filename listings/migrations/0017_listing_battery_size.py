# Generated manually for EV battery size.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0016_listing_drivetrain"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="battery_size",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
