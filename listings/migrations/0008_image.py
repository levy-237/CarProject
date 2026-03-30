from django.db import migrations, models
import django.db.models.deletion
import listings.models


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0007_alter_listing_body_type_alter_listing_brand_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to=listings.models.listing_image_upload_to),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="listings.listing",
                    ),
                ),
            ],
        ),
    ]
