from __future__ import annotations

from datetime import date  # noqa

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CASCADE, PROTECT
from lnschema_core import ids
from lnschema_core.fields import (
    BigIntegerField,
    BooleanField,
    CharField,
    DateField,
    EmailField,
    ForeignKey,
    TextField,
    URLField,
)
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


class Person(Record, CanCurate, TracksRun, TracksUpdates, ValidateFields):
    """Internal and external persons that can be a part of projects or references.

    Example:
        >>> person = Person(
        ...     name="Jane Doe",
        ...     email="jane.doe@example.com",
        ...     internal=True,
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str = CharField(db_index=True)
    """Name of the person (forename(s) lastname)."""
    email: str | None = EmailField(null=True, default=None)
    """Email of the person."""
    internal: bool = BooleanField(default=False)
    """Whether the person is internal to the organization or not."""


class Project(Record, CanCurate, TracksRun, TracksUpdates, ValidateFields):
    """Projects with associated persons and references.

    Example:
        >>> project = Project(
        ...     name="My Project Name",
        ...     abbr="MPN",
        ...     url="https://example.com/my_project",
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
    persons: Person = models.ManyToManyField(Person, related_name="project_persons")
    """Persons associated with this project."""
    references: Reference = models.ManyToManyField(
        "Reference", related_name="project_references"
    )
    """References associated with this project."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactProject", related_name="Projects"
    )
    """Artifacts labeled with this Project."""


class Reference(Record, CanCurate, TracksRun, TracksUpdates, ValidateFields):
    """References such as a publication or document, with unique identifiers and metadata.

    Example:
        >>> reference = Reference(
        ...     name="A Paper Title",
        ...     abbr="APT",
        ...     url="https://doi.org/10.1000/xyz123",
        ...     pubmed_id=12345678,
        ...     doi="10.1000/xyz123",
        ...     preprint=False,
        ...     journal="Nature Biotechnology",
        ...     description="A groundbreaking research paper.",
        ...     text="A really informative abstract.",
        ...     published_at=date(2023, 11, 21),
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    """Universal id, valid across DB instances."""
    name: str = CharField(db_index=True)
    """Title or name of the reference document."""
    abbr: str | None = CharField(
        max_length=32,
        db_index=True,
        unique=True,
        null=True,
    )
    """A unique abbreviation for the reference."""
    url: str | None = URLField(null=True, blank=True)
    """URL linking to the reference."""
    pubmed_id: int | None = BigIntegerField(null=True)
    """A PudMmed ID."""
    doi: int | None = CharField(
        null=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r"^(?:https?://(?:dx\.)?doi\.org/|doi:|DOI:)?10\.\d+/.*$",
                message="Must be a DOI (e.g., 10.1000/xyz123 or https://doi.org/10.1000/xyz123)",
            )
        ],
    )
    """Digital Object Identifier (DOI) for the reference."""
    preprint: bool = BooleanField(default=False)
    """Whether the reference is from a preprint."""
    journal: str | None = TextField(null=True)
    """Name of the journal."""
    description: str | None = TextField(null=True)
    """Description of the reference."""
    text: str | None = TextField(null=True)
    """Abstract or full text of the reference."""
    published_at: date = DateField(null=True, default=None)
    """Publication date."""
    persons: Person = models.ManyToManyField(Person, related_name="reference_persons")
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactReference", related_name="references"
    )
    """Artifacts labeled with this reference."""


class ArtifactReference(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_reference")
    reference: Reference = ForeignKey(Reference, PROTECT, related_name="links_artifact")
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactreference",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


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
