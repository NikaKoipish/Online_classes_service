# Generated by Django 5.0.6 on 2024-06-04 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="preview",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="courses/previews",
                verbose_name="превью курса",
            ),
        ),
    ]
