from django.db import models

class FundraisingAnnouncement(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    current_sum = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_sum = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to="announcement_images/", null=True, blank=True)
    operational_direction = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
