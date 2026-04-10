from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Report(models.Model):
    fundraising_announcement = models.ForeignKey("fundraisers.FundraisingAnnouncement", models.PROTECT)
    donation_document = models.FileField(upload_to="donation_documents/", blank=True, null=True)
    photo = models.ImageField(upload_to="report_photos/", blank=True, null=True)
    description = models.TextField()
    spent_sum = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(1)])
    date = models.DateField(auto_now_add=True)

    def clean(self):
        super().clean()
        if not (self.donation_document or self.photo):
            raise ValidationError("Звіт має містити акт приймання-передачі та/або фото передачі!")


    def __str__(self):
        return f"Звіт для {self.fundraising_announcement}"

    class Meta:
        verbose_name = "Звіт"
        verbose_name_plural = "Звіти"
