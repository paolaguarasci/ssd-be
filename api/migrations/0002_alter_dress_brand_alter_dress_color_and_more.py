# Generated by Django 4.1.3 on 2022-11-25 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dress",
            name="brand",
            field=models.IntegerField(
                choices=[(0, "GUCCI"), (1, "ARMANI"), (2, "VALENTINO")]
            ),
        ),
        migrations.AlterField(
            model_name="dress",
            name="color",
            field=models.IntegerField(
                choices=[
                    (0, "BLACK"),
                    (1, "BLUE"),
                    (2, "WHITE"),
                    (3, "RED"),
                    (4, "PINK"),
                    (5, "GRAY"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="dress",
            name="material",
            field=models.IntegerField(
                choices=[(0, "WOOL"), (1, "SILK"), (2, "COTTON")]
            ),
        ),
    ]
