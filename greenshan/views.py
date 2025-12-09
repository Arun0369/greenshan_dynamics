from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Project, Testimonial, Service, ContactRequest, ProjectMedia
from .forms import ProjectForm, ProjectMediaFormSet
from django.views.generic import DeleteView

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

# Public views
class HomeView(ListView):
    template_name = 'public/home.html'
    model = Project
    context_object_name = 'featured_projects'
    queryset = Project.objects.filter(featured=True)[:6]

class PortfolioListView(ListView):
    template_name = 'public/portfolio_list.html'
    model = Project
    context_object_name = 'projects'
    paginate_by = 12

class ProjectDetailView(DetailView):
    template_name = 'public/project_detail.html'
    model = Project
    slug_field = 'slug'
    context_object_name = 'project'

class ContactView(View):
    def get(self, request):
        return render(request, 'public/contact.html')
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subj = request.POST.get('subject','')
        msg = request.POST.get('message','')
        if not name or not email or not msg:
            messages.error(request, 'Please complete all required fields.')
            return redirect('portfolio_app:public_contact')
        ContactRequest.objects.create(name=name,email=email,subject=subj,message=msg)
        messages.success(request, 'Thanks — we received your message.')
        return redirect('portfolio_app:public_contact')

# Manage - staff only
staff_required = user_passes_test(is_staff_user, login_url=reverse_lazy('two_factor:login'))

@staff_required
def manage_dashboard(request):
    projects_count = Project.objects.count()
    media_count = ProjectMedia.objects.count()
    testimonials_count = Testimonial.objects.filter(visible=True).count()
    messages_count = ContactRequest.objects.filter(handled=False).count()
    context = {'projects_count': projects_count, 'media_count': media_count, 'testimonials_count': testimonials_count, 'messages_count': messages_count}
    return render(request, 'manage/dashboard.html', context)

@method_decorator(staff_required, name='dispatch')
class ManageProjectListView(ListView):
    template_name = 'manage/projects_list.html'
    model = Project
    context_object_name = 'projects'
    paginate_by = 20

@method_decorator(staff_required, name='dispatch')
class ManageProjectCreateView(View):
    template_name = 'manage/project_form.html'
    def get(self, request):
        form = ProjectForm()
        formset = ProjectMediaFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset, 'is_create': True})
    def post(self, request):
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            formset = ProjectMediaFormSet(request.POST, request.FILES, instance=project)
            if formset.is_valid():
                total_files = sum(1 for f in formset.cleaned_data if f and not f.get('DELETE', False))
                if total_files > 10:
                    project.delete()
                    messages.error(request, 'Maximum 10 media files per project allowed.')
                    return render(request, self.template_name, {'form': form, 'formset': formset, 'is_create': True})
                formset.save()
                messages.success(request, 'Project created.')
                return redirect('portfolio_app:manage_projects_list')
            else:
                project.delete()
        else:
            formset = ProjectMediaFormSet(request.POST, request.FILES)
        return render(request, self.template_name, {'form': form, 'formset': formset, 'is_create': True})

@method_decorator(staff_required, name='dispatch')
class ManageProjectUpdateView(View):
    template_name = 'manage/project_form.html'
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(instance=project)
        formset = ProjectMediaFormSet(instance=project)
        return render(request, self.template_name, {'form': form, 'formset': formset, 'project': project, 'is_create': False})
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        formset = ProjectMediaFormSet(request.POST, request.FILES, instance=project)
        if form.is_valid() and formset.is_valid():
            total_files = sum(1 for f in formset.cleaned_data if f and not f.get('DELETE', False))
            if total_files > 10:
                messages.error(request, 'Maximum 10 media files per project allowed.')
                return render(request, self.template_name, {'form': form, 'formset': formset, 'project': project, 'is_create': False})
            form.save()
            formset.save()
            messages.success(request, 'Project updated.')
            return redirect('portfolio_app:manage_projects_list')
        return render(request, self.template_name, {'form': form, 'formset': formset, 'project': project, 'is_create': False})

@method_decorator(staff_required, name='dispatch')
class ManageProjectDeleteView(DeleteView):
    model = Project
    template_name = 'manage/project_confirm_delete.html'
    success_url = reverse_lazy('portfolio_app:manage_projects_list')
