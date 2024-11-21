from __future__ import annotations

from django.db import models
from django.db.models import CASCADE, PROTECT
from lnschema_core import ids
from lnschema_core.fields import BooleanField, CharField, ForeignKey, URLField
from lnschema_core.models import (
    Artifact,
    CanCurate,
    Feature,
    LinkORM,
    Record,
    TracksRun,
    TracksUpdates,
    ValidateFields,
)


class Project(Record, CanCurate, TracksRun, TracksUpdates, ValidateFields):
    """Projects.

    Example:
        >>> Project = Project(
        ...     name="My project name",
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str = CharField(db_index=True)
    """Title or name of the Project."""
    abbr: str | None = CharField(max_length=32, db_index=True, unique=True, null=True)
    """A unique abbreviation."""
    url: str | None = URLField(max_length=255, null=True, default=None)
    """A URL to view."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactProject", related_name="Projects"
    )
    """Artifacts labeled with this Project."""


class ArtifactProject(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_project")
    project: Project = ForeignKey(Project, PROTECT, related_name="links_artifact")
    feature: Feature | None = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactproject",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)

    class Meta:
        # can have the same label linked to the same artifact if the feature is
        # different
        unique_together = ("artifact", "project", "feature")
