# F:\greenshan dynamics django\greenshan\urls.py

from django.urls import path, include
from .views import (
    home,
    services,
    portfolio,
    project_detail,
    about,
    testimonials,
    contact
)

app_name = "greenshan"

urlpatterns = [
    path("", home, name="home"),
    path("services/", services, name="services"),
    path("portfolio/", portfolio, name="portfolio"),
    path("about/", about, name="about"),
    path("testimonials/", testimonials, name="testimonials"),
    path("contact/", contact, name="contact"),
    path("project/<slug:slug>/", project_detail, name="project_detail"),
    path("accounts/", include("two_factor.urls")),
]
