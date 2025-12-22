from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Project,
    ProjectMedia,
    Testimonial,
    Service,
    ContactRequest,
)


# -------------------------------------------------
# Project Media Inline
# -------------------------------------------------

class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 1
    fields = ("preview", "file", "caption", "order")
    readonly_fields = ("preview",)
    ordering = ("order",)

    def preview(self, obj):
        if not obj.pk or not obj.file:
            return "—"
        if obj.media_type == ProjectMedia.MEDIA_IMAGE:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:6px;" />',
                obj.file.url,
            )
        return obj.filename

    preview.short_description = "Preview"


# -------------------------------------------------
# Project Admin
# -------------------------------------------------

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "project_date",
        "category",
        "featured",
        "created",
    )
    list_editable = ("featured",)
    list_filter = ("featured", "category", "created")
    search_fields = ("title", "client", "category")
    date_hierarchy = "created"
    inlines = [ProjectMediaInline]
    readonly_fields = ("created",)
    ordering = ("-created",)


# -------------------------------------------------
# Project Media Admin
# -------------------------------------------------

@admin.register(ProjectMedia)
class ProjectMediaAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "media_type",
        "order",
        "created",
    )
    list_filter = ("media_type", "created")
    list_editable = ("order",)
    search_fields = ("project__title",)
    ordering = ("project", "order")
    readonly_fields = ("created",)


# -------------------------------------------------
# Testimonial Admin
# -------------------------------------------------

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author", "position", "visible", "created")
    list_editable = ("visible",)
    list_filter = ("visible", "created")
    search_fields = ("author", "position")
    ordering = ("-created",)


# -------------------------------------------------
# Service Admin
# -------------------------------------------------

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    ordering = ("order",)


# -------------------------------------------------
# Contact Request Admin
# -------------------------------------------------

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "handled", "created")
    list_editable = ("handled",)
    list_filter = ("handled", "created")
    search_fields = ("name", "email", "subject")
    date_hierarchy = "created"
    ordering = ("-created",)
