from users.models import CustomUser
from django.db import models
import datetime

# Create your models here.
class Payment(models.Model):
    announcement = models.ForeignKey('fundraisers.FundraisingAnnouncement', on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    stripe_payment_intent = models.CharField(max_length=255, default='')
    is_finished = models.BooleanField(default=False)

    def __is_finished(self) -> str:
        return "✅" if self.is_finished else "❌"

    def __str__(self):
        return f"{datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')} -> {self.announcement} -> {self.__is_finished()}"