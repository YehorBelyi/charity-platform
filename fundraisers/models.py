"""Models that connect the fundraisers app to the database using Django ORM"""

from django.db import models

class FundraisingAnnouncement(models.Model):
    """
    Represents a fundraising announcement.

    Stores information about a fundraising campaign, including title, author,
    target and current amounts, description, optional photo, related unit,
    and status (open or closed).
    """

    #: Announcement title.
    title = models.CharField(max_length=300)
    #: User that created this announcement.
    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    #: Amount of money already collected.
    current_sum = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    #: Amount of money needed to reach the fundraising goal.
    target_sum = models.DecimalField(max_digits=12, decimal_places=2)
    #: Main information about the announcement.
    description = models.TextField()
    #: Photo representing the announcement.
    photo = models.ImageField(upload_to="announcement_images/", null=True, blank=True)
    #: The operational direction where the supported unit is deployed.
    operational_direction = models.CharField(max_length=100, null=True, blank=True)
    #: Foreign key to supported unit.
    unit = models.ForeignKey("units.Unit", on_delete=models.SET_NULL, null=True, blank=True)
    #: Indicates whether the announcement is closed or open for donations.
    is_closed = models.BooleanField(default=False)
    #: Date when the announcement was created.
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
