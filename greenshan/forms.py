from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from PIL import Image

from .models import Project, ProjectMedia, Testimonial


# -------------------------------------------------
# Constants
# -------------------------------------------------

MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100 MB

ALLOWED_EXT = {
    "image": ["jpg", "jpeg", "png", "webp", "gif"],
    "video": ["mp4", "webm", "mov", "ogg"],
    "audio": ["mp3", "wav", "m4a", "ogg"],
    "document": ["pdf", "doc", "docx", "ppt", "pptx", "txt"],
}

CATEGORY_CHOICES = [
    ("corporate", "Corporate"),
    ("motion", "Motion Graphics"),
    ("documentary", "Documentary"),
    ("social", "Social Media"),
    ("advertisement", "Advertisement"),
    ("other", "Other"),
]


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def detect_media_type_by_ext(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    for media_type, exts in ALLOWED_EXT.items():
        if ext in exts:
            return media_type
    return ProjectMedia.MEDIA_OTHER


def validate_file_size(file):
    if file.size > MAX_UPLOAD_SIZE:
        raise ValidationError(
            f"File too large (max {MAX_UPLOAD_SIZE // (1024 * 1024)} MB)."
        )


def validate_real_image(file):
    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        raise ValidationError("Upload a valid image file.")


# =================================================
# PROJECT FORM (FINAL)
# =================================================

class ProjectForm(forms.ModelForm):

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(),
    )

    class Meta:
        model = Project
        fields = [
            "title",
            "slug",
            "client",
            "project_date",
            "location",
            "category",
            "cover",
            "description",
            "experience_notes",
            "featured",
        ]
        widgets = {
            "project_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 6}),
            "experience_notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_cover(self):
        cover = self.cleaned_data.get("cover")
        if not cover:
            return cover
        validate_file_size(cover)
        validate_real_image(cover)
        return cover


# =================================================
# PROJECT MEDIA FORM
# =================================================

class ProjectMediaForm(forms.ModelForm):
    class Meta:
        model = ProjectMedia
        fields = ["file", "caption", "order"]

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if not file:
            return file
        validate_file_size(file)
        self.instance.media_type = detect_media_type_by_ext(file.name)
        return file


# =================================================
# TESTIMONIAL FORM
# =================================================

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["author", "position", "text", "visible"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }


# =================================================
# PROJECT MEDIA FORMSET
# =================================================

ProjectMediaFormSet = inlineformset_factory(
    Project,
    ProjectMedia,
    form=ProjectMediaForm,
    extra=1,
    can_delete=True,
)
