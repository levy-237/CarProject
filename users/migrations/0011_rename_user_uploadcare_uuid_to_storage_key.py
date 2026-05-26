from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_add_austrian_city_zipcodes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="uploadcare_uuid",
            new_name="storage_key",
        ),
        migrations.AlterField(
            model_name="user",
            name="storage_key",
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]
