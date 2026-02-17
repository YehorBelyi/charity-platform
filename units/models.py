from django.db import models

class Unit(models.Model):
    LEVEL_CHOICES = [
        ("agency", "Структура"),
        ("branch", "Рід військ"),
        ("corps", "Корпус"),
        ("brigade", "Бригада"),
        ("battalion", "Батальйон"),
        ("special", "Спецпідрозділ")
    ]

    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="units_logo/", null=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children"
    )
    level = models.CharField(max_length=40, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.name
