# Generated manually for drivetrain reference data.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0005_cardrivetrain"),
        ("listings", "0015_listing_model_trim"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="drivetrain",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="cars.cardrivetrain",
            ),
        ),
    ]
