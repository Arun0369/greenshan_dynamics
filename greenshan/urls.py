from django.urls import path
from . import views

app_name = "greenshan"

urlpatterns = [

    # =========================
    # PUBLIC PAGES
    # =========================
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services_view, name="services"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("contact/", views.contact, name="contact"),

    path(
        "project/<slug:slug>/",
        views.ProjectDetailView.as_view(),
        name="project_detail",
    ),

    # =========================
    # DASHBOARD
    # =========================
    path(
        "manage/dashboard/",
        views.manage_dashboard,
        name="dashboard",
    ),

    # =========================
    # PROJECT MANAGEMENT
    # =========================
    path(
        "manage/projects/",
        views.ManageProjectListView.as_view(),
        name="manage_list",
    ),
    path(
        "manage/projects/create/",
        views.ManageProjectCreateView.as_view(),
        name="manage_create",
    ),
    path(
        "manage/projects/<int:pk>/edit/",
        views.ManageProjectUpdateView.as_view(),
        name="manage_edit",
    ),
    path(
        "manage/projects/<int:pk>/delete/",
        views.delete_project,
        name="manage_delete",
    ),

    # =========================
    # TESTIMONIALS
    # =========================
    path(
        "manage/testimonials/",
        views.ManageTestimonialListView.as_view(),
        name="manage_testimonials",
    ),
    path(
        "manage/testimonials/<int:pk>/toggle/",
        views.toggle_testimonial_visibility,
        name="testimonial_toggle",
    ),
    path(
        "manage/testimonials/<int:pk>/delete/",
        views.delete_testimonial,
        name="testimonial_delete",
    ),

    # =========================
    # CONTACT MESSAGES
    # =========================
    path(
        "manage/messages/",
        views.ManageContactListView.as_view(),
        name="manage_messages",
    ),
    path(
        "manage/messages/<int:pk>/",
        views.ManageContactDetailView.as_view(),
        name="message_detail",
    ),
    path(
        "manage/messages/<int:pk>/handled/",
        views.mark_contact_handled,
        name="message_handled",
    ),
    path(
        "manage/messages/<int:pk>/delete/",
        views.delete_contact_message,
        name="message_delete",
    ),
]
