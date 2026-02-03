from django.contrib import admin
from verifications.models import VerificationRequest, VerificationDocument

# Register your models here.
class VerificationDocumentInline(admin.TabularInline):
    model = VerificationDocument
    extra = 0
    can_delete = False
    max_num = 0
    readonly_fields = ("file", "uploaded_at")

@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "requested_role", "status", "created_at")
    list_filter = ("status", "requested_role")
    inlines = [VerificationDocumentInline]
    readonly_fields = ("user", "requested_role", "created_at", "description")