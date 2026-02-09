from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST

from .models import (
    Project,
    ProjectMedia,
    Service,
    Testimonial,
    ContactRequest,
)
from .forms import (
    ProjectForm,
    ProjectMediaFormSet,
    TestimonialForm,
)

# =========================================================
# ACCESS CONTROL HELPERS
# =========================================================

def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def staff_required(view_func):
    return login_required(user_passes_test(is_staff_user)(view_func))


# =========================================================
# PUBLIC VIEWS
# =========================================================

def home(request):
    services = Service.objects.order_by("order")
    featured_projects = Project.objects.filter(featured=True)
    return render(
        request,
        "index.html",
        {
            "services": services,
            "featured_projects": featured_projects,
        },
    )


def about(request):
    return render(request, "greenshan/about.html")


def services_view(request):
    services = Service.objects.order_by("order")
    return render(
        request,
        "greenshan/services.html",
        {"services": services},
    )


def portfolio(request):
    projects = Project.objects.all()
    return render(
        request,
        "greenshan/portfolio.html",
        {"projects": projects},
    )


class ProjectDetailView(DetailView):
    model = Project
    template_name = "greenshan/detail.html"
    slug_field = "slug"
    context_object_name = "project"


# =========================================================
# CONTACT (PUBLIC)
# =========================================================

class ContactView(View):
    template_name = "greenshan/contact.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not name or not email or not message_text:
            messages.error(request, "All required fields must be filled.")
            return redirect("greenshan:contact")

        if len(message_text) > 2000:
            messages.error(request, "Message is too long.")
            return redirect("greenshan:contact")

        ContactRequest.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text,
        )

        messages.success(request, "Message sent successfully.")
        return redirect("greenshan:contact")


contact = ContactView.as_view()

# =========================================================
# DASHBOARD (STAFF ONLY)
# =========================================================

@staff_required
def manage_dashboard(request):
    return render(
        request,
        "manage/dashboard.html",
        {
            # Projects
            "projects_total": Project.objects.count(),
            "featured_projects": Project.objects.filter(featured=True).count(),

            # Media
            "media_count": ProjectMedia.objects.count(),

            # Testimonials
            "testimonials_total": Testimonial.objects.count(),
            "testimonials_visible": Testimonial.objects.filter(visible=True).count(),

            # Messages (pending only)
            "messages_pending": ContactRequest.objects.filter(handled=False).count(),
        },
    )



# =========================================================
# PROJECT MANAGEMENT (STAFF ONLY)
# =========================================================

@method_decorator(staff_required, name="dispatch")
class ManageProjectListView(ListView):
    model = Project
    template_name = "manage/project_list.html"
    context_object_name = "projects"
    paginate_by = 20

    def get_queryset(self):
        return Project.objects.order_by("-created")


@method_decorator(staff_required, name="dispatch")
class ManageProjectCreateView(View):
    template_name = "manage/project_form.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "form": ProjectForm(),
                "formset": ProjectMediaFormSet(),
                "is_create": True,
            },
        )

    def post(self, request):
        form = ProjectForm(request.POST, request.FILES)
        formset = ProjectMediaFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                project = form.save()
                formset.instance = project
                formset.save()
            messages.success(request, "Project created successfully.")
            return redirect("greenshan:manage_list")

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "formset": formset,
                "is_create": True,
            },
        )


@method_decorator(staff_required, name="dispatch")
class ManageProjectUpdateView(View):
    template_name = "manage/project_form.html"

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        return render(
            request,
            self.template_name,
            {
                "form": ProjectForm(instance=project),
                "formset": ProjectMediaFormSet(instance=project),
                "project": project,
                "is_create": False,
            },
        )

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        formset = ProjectMediaFormSet(request.POST, request.FILES, instance=project)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, "Project updated successfully.")
            return redirect("greenshan:manage_list")

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "formset": formset,
                "project": project,
                "is_create": False,
            },
        )


@staff_required
@require_POST
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    messages.success(request, "Project deleted.")
    return redirect("greenshan:manage_list")


# =========================================================
# TESTIMONIALS (STAFF ONLY)
# =========================================================

@method_decorator(staff_required, name="dispatch")
class ManageTestimonialListView(View):
    template_name = "manage/testimonials.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "testimonials": Testimonial.objects.order_by("-created"),
                "form": TestimonialForm(),
            },
        )

    def post(self, request):
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial added.")
        return redirect("greenshan:manage_testimonials")


@staff_required
@require_POST
def toggle_testimonial_visibility(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.visible = not testimonial.visible
    testimonial.save()
    return redirect("greenshan:manage_testimonials")


@staff_required
@require_POST
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    return redirect("greenshan:manage_testimonials")


# =========================================================
# CONTACT MESSAGES (STAFF ONLY)
# =========================================================

@method_decorator(staff_required, name="dispatch")
class ManageContactListView(ListView):
    model = ContactRequest
    template_name = "manage/messages.html"
    context_object_name = "contact_messages"


@method_decorator(staff_required, name="dispatch")
class ManageContactDetailView(View):
    template_name = "manage/message_detail.html"

    def get(self, request, pk):
        message = get_object_or_404(ContactRequest, pk=pk)
        return render(
            request,
            self.template_name,
            {"message": message},
        )


@staff_required
@require_POST
def mark_contact_handled(request, pk):
    message = get_object_or_404(ContactRequest, pk=pk)
    message.handled = True
    message.save()
    return redirect("greenshan:manage_messages")


@staff_required
@require_POST
def delete_contact_message(request, pk):
    message = get_object_or_404(ContactRequest, pk=pk)
    message.delete()
    return redirect("greenshan:manage_messages")
