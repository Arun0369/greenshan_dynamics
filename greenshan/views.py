from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Project, Testimonial, Service, ContactRequest, ProjectMedia
from .forms import (
    ProjectForm,
    ProjectMediaFormSet,
    TestimonialForm,
)

# ======================================================================
# PUBLIC VIEWS
# ======================================================================

def home(request):
    services = Service.objects.all().order_by("order")
    featured_projects = Project.objects.filter(featured=True).prefetch_related("media")
    return render(request, "index.html", {
        "services": services,
        "featured_projects": featured_projects,
    })


def about(request):
    return render(request, "public/about.html")


def services(request):
    services = Service.objects.all().order_by("order")
    return render(request, "public/services.html", {"services": services})


def portfolio(request):
    projects = Project.objects.prefetch_related("media")
    return render(request, "public/portfolio_list.html", {"projects": projects})


class ProjectDetailView(DetailView):
    model = Project
    template_name = "public/project_detail.html"
    slug_field = "slug"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.prefetch_related("media")

# ======================================================================
# CONTACT VIEW
# ======================================================================

class ContactView(View):
    template_name = "public/contact.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not email or not message:
            messages.error(request, "All required fields must be filled.")
            return redirect("greenshan:contact")

        ContactRequest.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        messages.success(request, "Message sent successfully.")
        return redirect("greenshan:contact")


contact = ContactView.as_view()

# ======================================================================
# STAFF / MANAGEMENT HELPERS
# ======================================================================

def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def staff_required(view_func):
    return login_required(
        user_passes_test(is_staff_user)(view_func),
        login_url="/accounts/login/",
    )

# ======================================================================
# STAFF / MANAGEMENT VIEWS
# ======================================================================

@staff_required
def manage_dashboard(request):
    context = {
        "projects_count": Project.objects.count(),
        "media_count": ProjectMedia.objects.count(),
        "testimonials_count": Testimonial.objects.filter(visible=True).count(),
        "messages_count": ContactRequest.objects.filter(handled=False).count(),
    }
    return render(request, "manage/dashboard.html", context)


@method_decorator(staff_required, name="dispatch")
class ManageProjectListView(ListView):
    model = Project
    template_name = "manage/projects_list.html"
    context_object_name = "projects"
    paginate_by = 20

    def get_queryset(self):
        return Project.objects.order_by("-created")


@method_decorator(staff_required, name="dispatch")
class ManageProjectCreateView(View):
    template_name = "manage/project_form.html"

    def get(self, request):
        return render(request, self.template_name, {
            "form": ProjectForm(),
            "formset": ProjectMediaFormSet(),
            "is_create": True,
        })

    def post(self, request):
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            with transaction.atomic():
                project = form.save()
                formset = ProjectMediaFormSet(request.POST, request.FILES, instance=project)

                if formset.is_valid():
                    total_files = sum(
                        1 for f in formset.cleaned_data if f and not f.get("DELETE", False)
                    )

                    if total_files > 10:
                        raise ValidationError("Maximum 10 media files allowed.")

                    formset.save()
                    messages.success(request, "Project created successfully.")
                    return redirect("greenshan:manage_projects")

        return render(request, self.template_name, {
            "form": form,
            "formset": ProjectMediaFormSet(),
            "is_create": True,
        })


@method_decorator(staff_required, name="dispatch")
class ManageProjectUpdateView(View):
    template_name = "manage/project_form.html"

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        return render(request, self.template_name, {
            "form": ProjectForm(instance=project),
            "formset": ProjectMediaFormSet(instance=project),
            "project": project,
            "is_create": False,
        })

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        formset = ProjectMediaFormSet(request.POST, request.FILES, instance=project)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                existing_count = project.media.count()
                new_files = sum(
                    1 for f in formset.cleaned_data if f and not f.get("DELETE", False)
                )

                if existing_count + new_files > 10:
                    messages.error(request, "Maximum 10 media files allowed.")
                else:
                    form.save()
                    formset.save()
                    messages.success(request, "Project updated successfully.")
                    return redirect("greenshan:manage_projects")

        return render(request, self.template_name, {
            "form": form,
            "formset": formset,
            "project": project,
            "is_create": False,
        })


@method_decorator(staff_required, name="dispatch")
class ManageProjectDeleteView(DeleteView):
    model = Project
    template_name = "manage/project_confirm_delete.html"
    success_url = reverse_lazy("greenshan:manage_projects")

# ======================================================================
# TESTIMONIAL MANAGEMENT
# ======================================================================

@method_decorator(staff_required, name="dispatch")
class ManageTestimonialListView(View):
    template_name = "manage/testimonials.html"

    def get(self, request):
        testimonials = Testimonial.objects.order_by("-created")
        form = TestimonialForm()
        return render(request, self.template_name, {
            "testimonials": testimonials,
            "form": form,
        })

    def post(self, request):
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial added successfully.")
        else:
            messages.error(request, "Failed to add testimonial.")
        return redirect("greenshan:manage_testimonials")


@staff_required
def toggle_testimonial_visibility(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.visible = not testimonial.visible
    testimonial.save()
    messages.success(request, "Testimonial visibility updated.")
    return redirect("greenshan:manage_testimonials")


@staff_required
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, "Testimonial deleted.")
    return redirect("greenshan:manage_testimonials")

# ======================================================================
# CONTACT MESSAGE MANAGEMENT
# ======================================================================

@method_decorator(staff_required, name="dispatch")
class ManageContactListView(ListView):
    model = ContactRequest
    template_name = "manage/messages.html"
    context_object_name = "messages"

    def get_queryset(self):
        return ContactRequest.objects.order_by("-created")


@method_decorator(staff_required, name="dispatch")
class ManageContactDetailView(View):
    template_name = "manage/message_detail.html"

    def get(self, request, pk):
        message = get_object_or_404(ContactRequest, pk=pk)
        return render(request, self.template_name, {"message": message})


@staff_required
def mark_contact_handled(request, pk):
    message = get_object_or_404(ContactRequest, pk=pk)
    message.handled = True
    message.save()
    messages.success(request, "Message marked as handled.")
    return redirect("greenshan:manage_messages")


@staff_required
def delete_contact_message(request, pk):
    message = get_object_or_404(ContactRequest, pk=pk)
    message.delete()
    messages.success(request, "Message deleted.")
    return redirect("greenshan:manage_messages")
