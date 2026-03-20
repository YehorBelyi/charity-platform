from django.contrib import admin
from users.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for CustomUser.

    Includes a custom column for verification status using visual indicators.
    """
    list_display = ("username", "email", "phone_number", "verification_status")

    def verification_status(self, obj):
        """
        Return an emoji representing the user's verification state.

        Args:
            obj (CustomUser): The user instance.
        """
        return "✅" if obj.is_verified() else "❌"

    verification_status.short_description = "Верифікація"