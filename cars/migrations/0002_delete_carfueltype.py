# Generated manually for EV-only listings.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CarFuelType",
        ),
    ]
