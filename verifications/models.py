from django.conf import settings
from django.db import models

# Create your models here.
class VerificationRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Обробка"
        APPROVED = "approved", "Підтверджено"
        REJECTED = "rejected", "Віхдилено"

    class Role(models.TextChoices):
        MILITARY = "military", "Військовий"
        VOLUNTEER = "volunteer", "Волонтер"
        FOUNDATION = "foundation", "Учасник благодійного фонду"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification_requests"
    )

    requested_role = models.CharField(
        max_length=20,
        choices=Role.choices,
        verbose_name="Хто ви?"
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    admin_comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="Деталі для верифікації/опис документів")

    def __str__(self):
        return f"{self.user} → {self.requested_role} ({self.status})"

class VerificationDocument(models.Model):
    request = models.ForeignKey(
        VerificationRequest,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    file = models.FileField(upload_to="verification_docs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
