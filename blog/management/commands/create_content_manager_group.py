from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создаёт группу «Контент-менеджер» и назначает ей права"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name="Контент-менеджер"
        )

        permissions = Permission.objects.filter(
            content_type__app_label="blog",
            content_type__model="article",
        )

        for permission in permissions:
            group.permissions.add(permission)

        if created:
            self.stdout.write(
                self.style.SUCCESS("Группа «Контент-менеджер» создана.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Группа «Контент-менеджер» уже существует.")
            )
