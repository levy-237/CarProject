from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0024_listing_heat_pump"),
    ]

    operations = [
        migrations.RenameField(
            model_name="image",
            old_name="uploadcare_uuid",
            new_name="storage_key",
        ),
        migrations.AlterField(
            model_name="image",
            name="storage_key",
            field=models.CharField(blank=True, db_index=True, max_length=255),
        ),
    ]
