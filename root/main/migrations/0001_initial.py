# Generated by Django 4.2.7 on 2023-12-11 06:26

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("image", models.ImageField(upload_to="static/main/img/cotigory-foto")),
            ],
        ),
        migrations.CreateModel(
            name="SubCategory",
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
                ("name", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("image", models.ImageField(upload_to="")),
                ("text", models.TextField(max_length=255)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.category"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Work",
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
                ("name", models.CharField(max_length=255)),
                ("image", models.ImageField(upload_to="static/main/img/work-foto")),
                ("title", models.CharField(max_length=255)),
                ("salary", models.DecimalField(decimal_places=2, max_digits=10)),
                ("vaqti", models.DateTimeField()),
                ("text", models.TextField(max_length=255)),
                ("desc", models.TextField(max_length=255)),
                ("status", models.BooleanField(default=True)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False, populate_from="title", unique=True
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.subcategory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JobApplication",
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
                ("name", models.CharField(max_length=255)),
                ("full_name", models.CharField(max_length=255)),
                ("phone_number", models.CharField(max_length=15)),
                ("resume", models.FileField(upload_to="static/main/resum ")),
                (
                    "work",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.work",
                    ),
                ),
            ],
        ),
    ]
