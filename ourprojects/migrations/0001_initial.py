# Generated by Django 5.1.3 on 2024-11-21 16:47

import django.core.validators
import django.db.models.deletion
import lamidb.base.ids
import lamidb.base.users
import lamindb.base.fields
import lamindb.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("lamindb", "0069_squashed"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtifactProject",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "label_ref_is_name",
                    lamindb.base.fields.BooleanField(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "feature_ref_is_name",
                    lamindb.base.fields.BooleanField(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "artifact",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_project",
                        to="lamindb.artifact",
                    ),
                ),
                (
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamidb.base.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "feature",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_artifactproject",
                        to="lamindb.feature",
                    ),
                ),
                (
                    "run",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.run",
                    ),
                ),
            ],
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.CreateModel(
            name="ArtifactReference",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "label_ref_is_name",
                    lamindb.base.fields.BooleanField(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "feature_ref_is_name",
                    lamindb.base.fields.BooleanField(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "artifact",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_reference",
                        to="lamindb.artifact",
                    ),
                ),
                (
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamidb.base.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "feature",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_artifactreference",
                        to="lamindb.feature",
                    ),
                ),
                (
                    "run",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.run",
                    ),
                ),
            ],
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "updated_at",
                    lamindb.base.fields.DateTimeField(auto_now=True, db_index=True),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=lamidb.base.ids.base62_8,
                        max_length=8,
                        unique=True,
                    ),
                ),
                (
                    "name",
                    lamindb.base.fields.CharField(
                        blank=True, db_index=True, default=None, max_length=255
                    ),
                ),
                (
                    "email",
                    lamindb.base.fields.EmailField(
                        blank=True, default=None, max_length=254, null=True
                    ),
                ),
                (
                    "external",
                    lamindb.base.fields.BooleanField(
                        blank=True, db_index=True, default=True
                    ),
                ),
                (
                    "_previous_runs",
                    models.ManyToManyField(related_name="+", to="lamindb.run"),
                ),
                (
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamidb.base.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "run",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.run",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                lamindb.models.CanCurate,
                models.Model,
                lamindb.models.ValidateFields,
            ),
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "updated_at",
                    lamindb.base.fields.DateTimeField(auto_now=True, db_index=True),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=lamidb.base.ids.base62_12,
                        max_length=12,
                        unique=True,
                    ),
                ),
                (
                    "name",
                    lamindb.base.fields.CharField(
                        blank=True, db_index=True, default=None, max_length=255
                    ),
                ),
                (
                    "abbr",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "url",
                    lamindb.base.fields.URLField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "_previous_runs",
                    models.ManyToManyField(related_name="+", to="lamindb.run"),
                ),
                (
                    "artifacts",
                    models.ManyToManyField(
                        related_name="projects",
                        through="ourprojects.ArtifactProject",
                        to="lamindb.artifact",
                    ),
                ),
                (
                    "contributors",
                    models.ManyToManyField(
                        related_name="projects", to="ourprojects.person"
                    ),
                ),
                (
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamidb.base.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "run",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.run",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                lamindb.models.CanCurate,
                models.Model,
                lamindb.models.ValidateFields,
            ),
        ),
        migrations.AddField(
            model_name="artifactproject",
            name="project",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="links_artifact",
                to="ourprojects.project",
            ),
        ),
        migrations.CreateModel(
            name="Reference",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "updated_at",
                    lamindb.base.fields.DateTimeField(auto_now=True, db_index=True),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=lamidb.base.ids.base62_12,
                        max_length=12,
                        unique=True,
                    ),
                ),
                (
                    "name",
                    lamindb.base.fields.CharField(
                        blank=True, db_index=True, default=None, max_length=255
                    ),
                ),
                (
                    "abbr",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("url", lamindb.base.fields.URLField(blank=True, null=True)),
                (
                    "pubmed_id",
                    lamindb.base.fields.BigIntegerField(
                        blank=True, db_index=True, null=True
                    ),
                ),
                (
                    "doi",
                    lamindb.base.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=255,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Must be a DOI (e.g., 10.1000/xyz123 or https://doi.org/10.1000/xyz123)",
                                regex="^(?:https?://(?:dx\\.)?doi\\.org/|doi:|DOI:)?10\\.\\d+/.*$",
                            )
                        ],
                    ),
                ),
                (
                    "preprint",
                    lamindb.base.fields.BooleanField(
                        blank=True, db_index=True, default=False
                    ),
                ),
                (
                    "public",
                    lamindb.base.fields.BooleanField(
                        blank=True, db_index=True, default=True
                    ),
                ),
                (
                    "journal",
                    lamindb.base.fields.TextField(blank=True, default=None, null=True),
                ),
                (
                    "description",
                    lamindb.base.fields.TextField(blank=True, default=None, null=True),
                ),
                (
                    "text",
                    lamindb.base.fields.TextField(blank=True, default=None, null=True),
                ),
                (
                    "published_at",
                    lamindb.base.fields.DateField(blank=True, default=None, null=True),
                ),
                (
                    "_previous_runs",
                    models.ManyToManyField(related_name="+", to="lamindb.run"),
                ),
                (
                    "artifacts",
                    models.ManyToManyField(
                        related_name="references",
                        through="ourprojects.ArtifactReference",
                        to="lamindb.artifact",
                    ),
                ),
                (
                    "authors",
                    models.ManyToManyField(
                        related_name="references", to="ourprojects.person"
                    ),
                ),
                (
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamidb.base.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "run",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.run",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                lamindb.models.CanCurate,
                models.Model,
                lamindb.models.ValidateFields,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="references",
            field=models.ManyToManyField(
                related_name="projects", to="ourprojects.reference"
            ),
        ),
        migrations.AddField(
            model_name="artifactreference",
            name="reference",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="links_artifact",
                to="ourprojects.reference",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="artifactproject",
            unique_together={("artifact", "project", "feature")},
        ),
        migrations.AlterUniqueTogether(
            name="artifactreference",
            unique_together={("artifact", "reference", "feature")},
        ),
    ]
