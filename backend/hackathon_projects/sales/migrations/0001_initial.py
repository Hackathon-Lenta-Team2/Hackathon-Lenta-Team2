# Generated by Django 4.2.5 on 2023-10-06 08:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import pathlib


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("stores", "0001_initial"),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FactSalesFile",
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
                    "file_path",
                    models.FileField(
                        help_text="файл в формате .csv",
                        upload_to=pathlib.PureWindowsPath(
                            "C:/C_DEV/1_All_together_build/Hackathon-Lenta"
                            "-Team2/backend/hackathon_projects/data"
                        ),
                        verbose_name="Файл для импорта",
                    ),
                ),
            ],
            options={
                "verbose_name": "Импорт фактических продаж",
                "verbose_name_plural": "Импорт фактических продаж",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="Sale",
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
                    "sku_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sales",
                        to="products.stockkeepingunit",
                        verbose_name="Товар",
                    ),
                ),
                (
                    "store_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sales",
                        to="stores.store",
                        verbose_name="Супермаркет",
                    ),
                ),
            ],
            options={
                "verbose_name": "Продажа",
                "verbose_name_plural": "Продажи",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="SaleInfo",
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
                ("date", models.DateField(verbose_name="Дата продажи")),
                (
                    "sales_type",
                    models.BooleanField(verbose_name="Флаг наличия промо"),
                ),
                (
                    "sales_units",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=15,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                        verbose_name="Число проданных товаров без признака "
                        "промо",
                    ),
                ),
                (
                    "sales_units_promo",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=15,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                        verbose_name="Число проданных товаров с признаком "
                        "промо",
                    ),
                ),
                (
                    "sales_rub",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=15,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                        verbose_name="Продажи без признака промо в рублях",
                    ),
                ),
                (
                    "sales_rub_promo",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=15,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                        verbose_name="Продажи с признаком промо в рублях",
                    ),
                ),
                (
                    "sale_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_info",
                        to="sales.sale",
                        verbose_name="Продажа",
                    ),
                ),
            ],
            options={
                "verbose_name": "Информация о продаже",
                "verbose_name_plural": "Информация о продажах",
                "ordering": ("date",),
            },
        ),
        migrations.AddConstraint(
            model_name="sale",
            constraint=models.UniqueConstraint(
                fields=("store_id", "sku_id"), name="unique_store_and_sku"
            ),
        ),
    ]
