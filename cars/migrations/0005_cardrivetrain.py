# Generated manually for drivetrain reference data.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0004_alter_carmodel_connected_brand_carmodeltrim"),
    ]

    operations = [
        migrations.CreateModel(
            name="CarDriveTrain",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
            ],
        ),
    ]
