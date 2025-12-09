from django import forms
from django.forms import inlineformset_factory
from .models import Project, ProjectMedia, Testimonial, Service, ContactRequest

MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100 MB

ALLOWED_EXT = {
    'image': ['jpg','jpeg','png','webp','gif'],
    'video': ['mp4','webm','mov','ogg'],
    'audio': ['mp3','wav','m4a','ogg'],
    'document': ['pdf','doc','docx','ppt','pptx','txt'],
}

def detect_media_type_by_ext(filename):
    ext = filename.rsplit('.',1)[-1].lower() if '.' in filename else ''
    for t, exts in ALLOWED_EXT.items():
        if ext in exts:
            return t
    return 'other'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','slug','client','project_date','location','category','cover','description','experience_notes','featured']
        widgets = {
            'project_date': forms.DateInput(attrs={'type':'date'}),
            'description': forms.Textarea(attrs={'rows':6}),
            'experience_notes': forms.Textarea(attrs={'rows':4}),
        }

class ProjectMediaForm(forms.ModelForm):
    class Meta:
        model = ProjectMedia
        fields = ['file','caption','order']

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if not f:
            return f
        if f.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(f"File too large (max {MAX_UPLOAD_SIZE//(1024*1024)} MB).")
        mtype = detect_media_type_by_ext(f.name)
        self.instance.media_type = mtype
        return f

ProjectMediaFormSet = inlineformset_factory(Project, ProjectMedia, form=ProjectMediaForm, extra=1, can_delete=True)
