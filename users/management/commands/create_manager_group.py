from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создает группу менеджеров и назначает ей необходимые права доступа"

    def handle(self, *args, **kwargs):
        manager_group = Group.objects.create(name="Manager")

        block_permission = Permission.objects.get(codename="can_block_user")
        cancel_permission = Permission.objects.get(codename="can_cancel_mailing")

        manager_group.permissions.add(block_permission, cancel_permission)

        manager_group.save()
