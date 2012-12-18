from django.core.management.base import BaseCommand

from readthedocs.builds.models import Version
from readthedocs.projects.tasks import update_intersphinx


class Command(BaseCommand):
    def handle(self, *args, **options):
        for version in Version.objects.filter(slug="latest"):
            update_intersphinx(version.pk)
