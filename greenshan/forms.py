from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from PIL import Image

from .models import Project, ProjectMedia, Testimonial


# =================================================
# PROJECT FORM
# =================================================

class ProjectForm(forms.ModelForm):
    """
    Main form for creating and editing projects.
    """

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Slug is auto-generated; keep it optional and safe
        self.fields["slug"].required = False
        self.fields["slug"].widget.attrs["readonly"] = True

    def clean_cover(self):
        """
        Extra safety check to ensure uploaded cover is a valid image.
        """
        cover = self.cleaned_data.get("cover")
        if not cover:
            return cover

        try:
            img = Image.open(cover)
            img.verify()
        except Exception:
            raise ValidationError("Upload a valid image file.")

        return cover


# =================================================
# PROJECT MEDIA FORM
# =================================================

class ProjectMediaForm(forms.ModelForm):
    """
    Individual media item form.
    Core validation is handled in the model.
    """

    class Meta:
        model = ProjectMedia
        fields = ["file", "media_type", "caption", "order"]

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")
        media_type = cleaned_data.get("media_type")

        if file and not media_type:
            raise ValidationError("Media type is required.")

        return cleaned_data


# =================================================
# PROJECT MEDIA FORMSET
# =================================================

class BaseProjectMediaFormSet(forms.BaseInlineFormSet):
    """
    Enforces business rules across all media:
    - Maximum 10 media files per project
    """

    def clean(self):
        super().clean()

        active_forms = [
            form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        ]

        if len(active_forms) > 10:
            raise ValidationError(
                "A project can have a maximum of 10 media files."
            )


ProjectMediaFormSet = inlineformset_factory(
    Project,
    ProjectMedia,
    form=ProjectMediaForm,
    formset=BaseProjectMediaFormSet,
    extra=1,
    can_delete=True,
)


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
