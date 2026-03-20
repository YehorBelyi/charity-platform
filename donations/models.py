from users.models import CustomUser
from django.db import models
import datetime

# Create your models here.
class Payment(models.Model):
    """
    Represents a donation or payment transaction within the system.

    This model stores Stripe transaction details, links the payment to a
    specific fundraising announcement, and tracks its completion status.
    """

    #: Reference to the related fundraising announcement.
    announcement = models.ForeignKey('fundraisers.FundraisingAnnouncement', on_delete=models.CASCADE, related_name='payments')
    #: The user who made the payment. Can be null for anonymous donations.
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    #: The amount of money donated (supports up to 10 digits, 2 decimal places).
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    #: The date when the payment record was created.
    date = models.DateField(auto_now_add=True)
    #: Unique identifier for the transaction in the Stripe system.
    stripe_payment_intent = models.CharField(max_length=255, default='')
    #: Flag indicating whether the payment was successfully processed.
    is_finished = models.BooleanField(default=False)


    def __is_finished(self) -> str:
        """
        Returns an emoji representation of the payment status.

        Returns:
            str: "✅" if finished, "❌" otherwise.
        """
        return "✅" if self.is_finished else "❌"

    def __str__(self):
        return f"{datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')} -> {self.announcement} -> {self.__is_finished()}"