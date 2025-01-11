from __future__ import annotations

from datetime import date  # noqa

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CASCADE, PROTECT
from lamindb.base import ids
from lamindb.base.fields import (
    BigIntegerField,
    BooleanField,
    CharField,
    DateField,
    EmailField,
    ForeignKey,
    TextField,
    URLField,
)
from lamindb.models import (
    Artifact,
    BasicRecord,
    CanCurate,
    Collection,
    Feature,
    LinkORM,
    Record,
    TracksRun,
    TracksUpdates,
    Transform,
    ValidateFields,
)


class Person(Record, CanCurate, TracksRun, TracksUpdates, ValidateFields):
    """Internal and external people that can be a part of projects or references.

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
    uid: str = CharField(unique=True, max_length=8, db_index=True, default=ids.base62_8)
    """Universal id, valid across DB instances."""
    name: str = CharField(db_index=True)
    """Name of the person (forename(s) lastname)."""
    email: str | None = EmailField(null=True, default=None)
    """Email of the person."""
    external: bool = BooleanField(default=True, db_index=True)
    """Whether the person is external to the organization."""


class Project(Record, CanCurate, TracksRun, TracksUpdates, ValidateFields):
    """Projects with associated people and references.

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
    uid: str = CharField(
        unique=True, max_length=12, db_index=True, default=ids.base62_12
    )
    """Universal id, valid across DB instances."""
    name: str = CharField(db_index=True)
    """Title or name of the Project."""
    abbr: str | None = CharField(max_length=32, db_index=True, unique=True, null=True)
    """A unique abbreviation."""
    url: str | None = URLField(max_length=255, null=True, default=None)
    """A URL to view."""
    contributors: Person = models.ManyToManyField(Person, related_name="projects")
    """Contributors associated with this project."""
    references: Reference = models.ManyToManyField("Reference", related_name="projects")
    """References associated with this project."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactProject", related_name="projects"
    )
    """Artifacts labeled with this Project."""
    transforms: Transform = models.ManyToManyField(
        Transform, through="TransformProject", related_name="projects"
    )
    """Transforms labeled with this project."""
    collections: Collection = models.ManyToManyField(
        Collection, through="CollectionProject", related_name="projects"
    )
    """Collections labeled with this project."""


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
    uid: str = CharField(
        unique=True, max_length=12, db_index=True, default=ids.base62_12
    )
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
    url: str | None = URLField(null=True)
    """URL linking to the reference."""
    pubmed_id: int | None = BigIntegerField(null=True, db_index=True)
    """A PudMmed ID."""
    doi: str | None = CharField(
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
    preprint: bool = BooleanField(default=False, db_index=True)
    """Whether the reference is from a preprint."""
    public: bool = BooleanField(default=True, db_index=True)
    """Whether the reference is public."""
    journal: str | None = TextField(null=True)
    """Name of the journal."""
    description: str | None = TextField(null=True)
    """Description of the reference."""
    text: str | None = TextField(null=True)
    """Abstract or full text of the reference."""
    published_at: date | None = DateField(null=True, default=None)
    """Publication date."""
    authors: Person = models.ManyToManyField(Person, related_name="references")
    """All people associated with this reference."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactReference", related_name="references"
    )
    """Artifacts labeled with this reference."""
    transforms: Artifact = models.ManyToManyField(
        Transform, through="TransformReference", related_name="references"
    )
    """Transforms labeled with this reference."""
    collections: Artifact = models.ManyToManyField(
        Collection, through="CollectionReference", related_name="references"
    )
    """Collections labeled with this reference."""


class ArtifactProject(BasicRecord, LinkORM, TracksRun):
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
        # can have the same label linked to the same artifact if the feature is different
        unique_together = ("artifact", "project", "feature")


class TransformProject(BasicRecord, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    transform: Transform = ForeignKey(Transform, CASCADE, related_name="links_project")
    project: Project = ForeignKey(Project, PROTECT, related_name="links_transform")

    class Meta:
        unique_together = ("transform", "project")


class CollectionProject(BasicRecord, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    collection: Collection = ForeignKey(
        Collection, CASCADE, related_name="links_project"
    )
    project: Project = ForeignKey(Project, PROTECT, related_name="links_collection")

    class Meta:
        unique_together = ("collection", "project")


class ArtifactReference(BasicRecord, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_reference")
    reference: Reference = ForeignKey(Reference, PROTECT, related_name="links_artifact")
    feature: Feature | None = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactreference",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)

    class Meta:
        # can have the same label linked to the same artifact if the feature is different
        unique_together = ("artifact", "reference", "feature")


class TransformReference(BasicRecord, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    transform: Transform = ForeignKey(
        Transform, CASCADE, related_name="links_reference"
    )
    reference: Reference = ForeignKey(
        Reference, PROTECT, related_name="links_transform"
    )

    class Meta:
        unique_together = ("transform", "reference")


class CollectionReference(BasicRecord, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    collection: Collection = ForeignKey(
        Collection, CASCADE, related_name="links_reference"
    )
    reference: Reference = ForeignKey(
        Reference, PROTECT, related_name="links_collection"
    )

    class Meta:
        unique_together = ("collection", "reference")
