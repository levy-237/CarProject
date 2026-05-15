# Generated manually for EV-only listings.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0013_remove_listing_fuel"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listing",
            name="transmission",
        ),
    ]
