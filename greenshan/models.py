from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import os


# -------------------------------------------------
# Upload path helpers
# -------------------------------------------------

def upload_to_project_cover(instance, filename):
    slug = instance.slug or "new"
    return os.path.join("projects", slug, "cover", filename)


def upload_to_project_media(instance, filename):
    slug = (
        instance.project.slug
        if instance.project and instance.project.slug
        else f"project-{instance.project_id or 'x'}"
    )
    return os.path.join("projects", slug, "media", filename)


# -------------------------------------------------
# PROJECT MODEL (SINGLE SOURCE OF TRUTH)
# -------------------------------------------------

class Project(models.Model):

    CATEGORY_CHOICES = [
        ("corporate", "Corporate"),
        ("motion", "Motion Graphics"),
        ("documentary", "Documentary"),
        ("social", "Social Media"),
        ("advertisement", "Advertisement"),
        ("branding", "Branding"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    client = models.CharField(max_length=200, blank=True)
    project_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)

    category = models.CharField(
        max_length=120,
        choices=CATEGORY_CHOICES,
        blank=True,
        db_index=True,
    )

    cover = models.ImageField(
        upload_to=upload_to_project_cover,
        null=True,
        blank=True,
    )

    description = models.TextField(blank=True)
    experience_notes = models.TextField(blank=True)

    featured = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-project_date", "-created"]
        indexes = [
            models.Index(fields=["featured"]),
            models.Index(fields=["category"]),
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate unique slug
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "greenshan:project_detail",
            kwargs={"slug": self.slug},
        )


# -------------------------------------------------
# PROJECT MEDIA MODEL
# -------------------------------------------------

class ProjectMedia(models.Model):

    MEDIA_IMAGE = "image"
    MEDIA_VIDEO = "video"
    MEDIA_AUDIO = "audio"
    MEDIA_DOCUMENT = "document"
    MEDIA_OTHER = "other"

    MEDIA_CHOICES = [
        (MEDIA_IMAGE, "Image"),
        (MEDIA_VIDEO, "Video"),
        (MEDIA_AUDIO, "Audio"),
        (MEDIA_DOCUMENT, "Document"),
        (MEDIA_OTHER, "Other"),
    ]

    project = models.ForeignKey(
        Project,
        related_name="media",
        on_delete=models.CASCADE,
    )

    file = models.FileField(upload_to=upload_to_project_media)
    media_type = models.CharField(
        max_length=20,
        choices=MEDIA_CHOICES,
        default=MEDIA_OTHER,
    )

    caption = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created"]
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["media_type"]),
        ]

    def __str__(self):
        return f"{self.project.title} — {self.media_type}"

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def is_image(self):
        return self.media_type == self.MEDIA_IMAGE

    def is_video(self):
        return self.media_type == self.MEDIA_VIDEO

    def is_audio(self):
        return self.media_type == self.MEDIA_AUDIO

    def is_document(self):
        return self.media_type == self.MEDIA_DOCUMENT


# -------------------------------------------------
# TESTIMONIAL MODEL
# -------------------------------------------------

class Testimonial(models.Model):
    author = models.CharField(max_length=120)
    position = models.CharField(max_length=120, blank=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["visible"]),
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"{self.author} — {self.position or 'Client'}"


# -------------------------------------------------
# SERVICE MODEL
# -------------------------------------------------

class Service(models.Model):
    title = models.CharField(max_length=160)
    summary = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


# -------------------------------------------------
# CONTACT REQUEST MODEL
# -------------------------------------------------

class ContactRequest(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=250, blank=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["handled"]),
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"{self.name} — {self.email} ({self.created.date()})"
