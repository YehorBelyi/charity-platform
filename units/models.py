from django.db import models

class Unit(models.Model):
    """
    Represents a military or organizational unit.

    This model supports a hierarchical structure (tree) where units can have
    parent and child relationships (e.g., a Battalion belongs to a Brigade).
    """

    #: Choices for the organizational level of the unit.
    LEVEL_CHOICES = [
        ("agency", "Структура"),
        ("branch", "Рід військ"),
        ("corps", "Корпус"),
        ("brigade", "Бригада"),
        ("battalion", "Батальйон"),
        ("special", "Спецпідрозділ")
    ]

    #: Full name of the unit.
    name = models.CharField(max_length=150)

    #: Official logo or emblem of the unit.
    logo = models.ImageField(upload_to="units_logo/", null=True, blank=True)
    #: Brief summary for previews (max 300 characters).
    short_description = models.CharField(max_length=300, blank=True)
    #: Detailed historical or operational description.
    description = models.TextField()
    #: Self-referential foreign key to create a hierarchy.
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children"
    )
    #: The category or depth level in the organizational tree.
    level = models.CharField(max_length=40, choices=LEVEL_CHOICES)

    def __str__(self):
        """Returns the unit name for representation."""
        return self.name
