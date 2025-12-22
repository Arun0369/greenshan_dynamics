from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "greenshan"

urlpatterns = [
    # =======================
    # PUBLIC PAGES
    # =======================
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path(
        "project/<slug:slug>/",
        views.ProjectDetailView.as_view(),
        name="project_detail",
    ),

    # =======================
    # MANAGEMENT (STAFF)
    # =======================
    path("manage/", views.manage_dashboard, name="manage_dashboard"),

    # Projects
    path(
        "manage/projects/",
        views.ManageProjectListView.as_view(),
        name="manage_projects",
    ),
    path(
        "manage/projects/add/",
        views.ManageProjectCreateView.as_view(),
        name="manage_project_add",
    ),
    path(
        "manage/projects/<int:pk>/edit/",
        views.ManageProjectUpdateView.as_view(),
        name="manage_project_edit",
    ),
    path(
        "manage/projects/<int:pk>/delete/",
        views.ManageProjectDeleteView.as_view(),
        name="manage_project_delete",
    ),

    # Testimonials
    path(
        "manage/testimonials/",
        views.ManageTestimonialListView.as_view(),
        name="manage_testimonials",
    ),
    path(
        "manage/testimonials/<int:pk>/toggle/",
        views.toggle_testimonial_visibility,
        name="toggle_testimonial",
    ),
    path(
        "manage/testimonials/<int:pk>/delete/",
        views.delete_testimonial,
        name="delete_testimonial",
    ),

    # Contact Messages
    path(
        "manage/messages/",
        views.ManageContactListView.as_view(),
        name="manage_messages",
    ),
    path(
        "manage/messages/<int:pk>/",
        views.ManageContactDetailView.as_view(),
        name="manage_message_detail",
    ),
    path(
        "manage/messages/<int:pk>/handled/",
        views.mark_contact_handled,
        name="mark_message_handled",
    ),
    path(
        "manage/messages/<int:pk>/delete/",
        views.delete_contact_message,
        name="delete_message",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
