# Generated by Django 4.1.5 on 2023-02-05 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("librephotos", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("USER", "User Labelled"),
                            ("CLUSTER", "Cluster ID"),
                            ("UNKNOWN", "Unknown Person"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "cluster_owner",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=models.SET(users.models.UserMixin.get_deleted_user),
                        related_name="owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "cover_photo",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="person",
                        to="librephotos.photo",
                    ),
                ),
            ],
        ),
    ]
