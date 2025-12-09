from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from greenshan.models import Project, Testimonial, Service, ContactRequest

class Command(BaseCommand):
    help = 'Create default groups: Admin, Editor, Viewer and assign permissions'

    def handle(self, *args, **options):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        editor_group, _ = Group.objects.get_or_create(name='Editor')
        viewer_group, _ = Group.objects.get_or_create(name='Viewer')

        models = [Project, Testimonial, Service, ContactRequest]
        for model in models:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct)
            for p in perms:
                admin_group.permissions.add(p)
            # Editor: add add/change/delete
            for codename in ['add','change','delete']:
                perm = Permission.objects.filter(content_type=ct, codename__startswith=codename).first()
                if perm:
                    editor_group.permissions.add(perm)
            # Viewer: view permission if exists
            view_perm = Permission.objects.filter(content_type=ct, codename__startswith='view').first()
            if view_perm:
                viewer_group.permissions.add(view_perm)

        self.stdout.write(self.style.SUCCESS('Groups Admin, Editor, Viewer created/updated.'))
