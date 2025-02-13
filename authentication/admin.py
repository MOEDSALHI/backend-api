from django.apps import apps
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    """Ensure default user groups exist with the right permissions."""
    if sender.name != "authentication":
        print(f"Skipping {sender.name}")
        return

    print("Running post_migrate for authentication...")

    # Create groups
    clients_group, _ = Group.objects.get_or_create(name="Clients")
    staff_group, _ = Group.objects.get_or_create(name="Staff")

    # Ensure the required permissions exist before assigning them
    models = ["Reference", "Bar", "Stock", "Order"]
    for model_name in models:
        model = apps.get_model("bar", model_name)
        content_type = ContentType.objects.get_for_model(model)

        permissions = Permission.objects.filter(content_type=content_type)
        staff_group.permissions.add(*permissions)

    print("User groups created: Clients & Staff with appropriate permissions")
