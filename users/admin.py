from django.contrib import admin
from users.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone_number", "verification_status")

    def verification_status(self, obj):
        return "✅" if obj.is_verified() else "❌"

    verification_status.short_description = "Верифікація"