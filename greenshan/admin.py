from django.contrib import admin
from .models import Project, ProjectMedia, Testimonial, Service, ContactRequest

class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 1
    readonly_fields = ('file',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','client','project_date','category','featured')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectMediaInline]
    search_fields = ('title','client','category')
    list_filter = ('category','featured')

@admin.register(ProjectMedia)
class ProjectMediaAdmin(admin.ModelAdmin):
    list_display = ('project','media_type','filename','order')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author','position','visible','created')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title','order')

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name','email','subject','created','handled')
    list_filter = ('handled',)
