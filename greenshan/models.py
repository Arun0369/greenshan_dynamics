from django.db import models
from django.urls import reverse
import os

def upload_to_project_cover(instance, filename):
    slug = instance.slug or str(instance.id or 'new')
    return os.path.join('projects', slug, 'cover', filename)

def upload_to_project_media(instance, filename):
    slug = instance.project.slug if instance.project and instance.project.slug else f'project-{instance.project_id or "x"}'
    return os.path.join('projects', slug, 'media', filename)

class Project(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    client = models.CharField(max_length=200, blank=True)
    project_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=120, blank=True)
    cover = models.ImageField(upload_to=upload_to_project_cover, null=True, blank=True)
    description = models.TextField(blank=True)
    experience_notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-project_date', '-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio_app:project_detail', kwargs={'slug': self.slug})


class ProjectMedia(models.Model):
    MEDIA_IMAGE = 'image'
    MEDIA_VIDEO = 'video'
    MEDIA_AUDIO = 'audio'
    MEDIA_DOCUMENT = 'document'
    MEDIA_OTHER = 'other'

    MEDIA_CHOICES = [
        (MEDIA_IMAGE, 'Image'),
        (MEDIA_VIDEO, 'Video'),
        (MEDIA_AUDIO, 'Audio'),
        (MEDIA_DOCUMENT, 'Document'),
        (MEDIA_OTHER, 'Other'),
    ]

    project = models.ForeignKey(Project, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to_project_media)
    media_type = models.CharField(max_length=20, choices=MEDIA_CHOICES, default=MEDIA_OTHER)
    caption = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created']

    def __str__(self):
        return f"{self.project.title} — {self.media_type} ({self.file.name})"

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


class Testimonial(models.Model):
    author = models.CharField(max_length=120)
    position = models.CharField(max_length=120, blank=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.author} — {self.position or 'Client'}"


class Service(models.Model):
    title = models.CharField(max_length=160)
    summary = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ContactRequest(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=250, blank=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.name} — {self.email} ({self.created.date()})"
