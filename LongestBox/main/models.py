from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Box(models.Model):
    name = models.CharField(max_length=200)
    sImg = models.ImageField(upload_to="boxes")

    def __str__(self):
        return self.name  # pylint: disable=no-member

    # This Meta class will remove the automatic pluralisation in the admin page, it adds an 'S' so it said boxs.
    # Now it will say Boxes.
    class Meta:
        verbose_name_plural = "Boxes"


class Comic(models.Model):
    PUBLISHER = "Publisher"
    ASPEN_COMICS = "Aspen Comics"
    DC_COMICS = "DC Comics"
    DARK_HORSE = "Dark Horse"
    IMAGE_COMICS = "Image Comics"
    MARVEL = "Marvel"

    PUBLISHER_CHOICES = [
        (PUBLISHER, "Publisher"),
        (ASPEN_COMICS, "Aspen Comics"),
        (DC_COMICS, "DC Comics"),
        (DARK_HORSE, "Dark Horse"),
        (IMAGE_COMICS, "Image comics"),
        (MARVEL, "Marvel"),
    ]
    publisher = models.CharField(
        max_length=50, choices=PUBLISHER_CHOICES, default=PUBLISHER,
    )

    def is_upperclass(self):
        return self.publisher in {self.MARVEL, self.DC_COMICS}

    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    name = models.CharField("Title", max_length=120)
    sImg = models.ImageField("Image", upload_to="comics/")
    number = models.PositiveSmallIntegerField()
    date = models.DateField()
    condition = models.CharField("Condition", max_length=5)
    owned = models.BooleanField("I own this comic.", default=True)
    variant = models.CharField("Variant", max_length=5)
    owned = models.BooleanField()
