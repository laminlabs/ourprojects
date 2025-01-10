# Generated by Django 5.2 on 2025-01-07 14:37

import django.db.models.deletion
import lamindb.base.fields
import lamindb.base.users
import lamindb.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ourprojects", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="_branch_code",
            field=models.SmallIntegerField(db_index=True, default=1, db_default=1),
        ),
        migrations.AddField(
            model_name="project",
            name="_branch_code",
            field=models.SmallIntegerField(db_index=True, default=1, db_default=1),
        ),
        migrations.AddField(
            model_name="reference",
            name="_branch_code",
            field=models.SmallIntegerField(db_index=True, default=1, db_default=1),
        ),
        migrations.AddField(
            model_name="person",
            name="aux",
            field=models.JSONField(default=None, db_default=None, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="aux",
            field=models.JSONField(default=None, db_default=None, null=True),
        ),
        migrations.AddField(
            model_name="reference",
            name="aux",
            field=models.JSONField(default=None, db_default=None, null=True),
        ),
        migrations.CreateModel(
            name="CollectionProject",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "collection",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_project",
                        to="lamindb.collection",
                    ),
                ),
                (
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.base.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "project",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_collection",
                        to="ourprojects.project",
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
                "unique_together": {("collection", "project")},
            },
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.AddField(
            model_name="project",
            name="collections",
            field=models.ManyToManyField(
                related_name="projects",
                through="ourprojects.CollectionProject",
                to="lamindb.collection",
            ),
        ),
        migrations.CreateModel(
            name="CollectionReference",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "collection",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_reference",
                        to="lamindb.collection",
                    ),
                ),
                (
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.base.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "reference",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_collection",
                        to="ourprojects.reference",
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
                "unique_together": {("collection", "reference")},
            },
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.AddField(
            model_name="reference",
            name="collections",
            field=models.ManyToManyField(
                related_name="references",
                through="ourprojects.CollectionReference",
                to="lamindb.collection",
            ),
        ),
        migrations.CreateModel(
            name="TransformProject",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.base.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "project",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_transform",
                        to="ourprojects.project",
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
                (
                    "transform",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_project",
                        to="lamindb.transform",
                    ),
                ),
            ],
            options={
                "unique_together": {("transform", "project")},
            },
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.AddField(
            model_name="project",
            name="transforms",
            field=models.ManyToManyField(
                related_name="projects",
                through="ourprojects.TransformProject",
                to="lamindb.transform",
            ),
        ),
        migrations.CreateModel(
            name="TransformReference",
            fields=[
                (
                    "created_at",
                    lamindb.base.fields.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "created_by",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        default=lamindb.base.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lamindb.user",
                    ),
                ),
                (
                    "reference",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_transform",
                        to="ourprojects.reference",
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
                (
                    "transform",
                    lamindb.base.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_reference",
                        to="lamindb.transform",
                    ),
                ),
            ],
            options={
                "unique_together": {("transform", "reference")},
            },
            bases=(lamindb.models.LinkORM, models.Model),
        ),
        migrations.AddField(
            model_name="reference",
            name="transforms",
            field=models.ManyToManyField(
                related_name="references",
                through="ourprojects.TransformReference",
                to="lamindb.transform",
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AddField(
            model_name="reference",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.RemoveField(
            model_name="person",
            name="_previous_runs",
        ),
        migrations.RemoveField(
            model_name="project",
            name="_previous_runs",
        ),
        migrations.RemoveField(
            model_name="reference",
            name="_previous_runs",
        ),
    ]
