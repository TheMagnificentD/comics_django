import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.


class Box(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    sImg = models.ImageField(upload_to="boxes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    CON = "Condition"
    GM = "Gem Mint (10)"
    MI = "Mint (9.9)"
    NMMI = "Near Mint / Mint (9.8)"
    NMP = "Near Mint+ (9.6)"
    NM = "Near Mint (9.4)"
    NMM = "Near Mint- (9.2)"
    VFNM = "Very Fine / Near Mint+ (9.0)"
    VFP = "Very Fine+ (8.5)"
    VF = "Very Fine (8.0)"
    VFM = "Very Fine- (7.5)"
    FNVF = "Fine / Very Fine (7.0)"
    FNP = "Fine+ (6.5)"
    FN = "Fine (6.0)"
    FNM = "Fine- (5.5)"
    VGFN = "Very Good / Fine (5.0)"
    VGP = "Very Good+ (4.5)"
    VG = "Very Good (4.0)"
    VGM = "Very Good- (3.5)"
    GOVG = "Good / Very Good+ (3.0)"
    GOP = "Good+ (2.5)"
    GO = "Good (2.0)"
    GOM = "Good- (1.8)"
    FAGO = "Fair / Good (1.5)"
    FA = "Fair (1.0)"
    PO = "Poor (0.5)"

    CONDITION_CHOICES = [
        (CON, "Condition"),
        (GM, "Gem Mint (10)"),
        (MI, "Mint (9.9)"),
        (NMMI, "Near Mint / Mint (9.8)"),
        (NMP, "Near Mint+ (9.6)"),
        (NM, "Near Mint (9.4)"),
        (NMM, "Near Mint- (9.2)"),
        (VFNM, "Very Fine / Near Mint+ (9.0)"),
        (VFP, "Very Fine+ (8.5)"),
        (VF, "Very Fine (8.0)"),
        (VFM, "Very Fine- (7.5)"),
        (FNVF, "Fine / Very Fine (7.0)"),
        (FNP, "Fine+ (6.5)"),
        (FN, "Fine (6.0)"),
        (FNM, "Fine- (5.5)"),
        (VGFN, "Very Good / Fine (5.0)"),
        (VGP, "Very Good+ (4.5)"),
        (VG, "Very Good (4.0)"),
        (VGM, "Very Good- (3.5)"),
        (GOVG, "Good / Very Good+ (3.0)"),
        (GOP, "Good+ (2.5)"),
        (GO, "Good (2.0)"),
        (GOM, "Good- (1.8)"),
        (FAGO, "Fair / Good (1.5)"),
        (FA, "Fair (1.0)"),
        (PO, "Poor (0.5)"),
    ]

    publisher = models.CharField(
        max_length=50, choices=PUBLISHER_CHOICES, default=PUBLISHER,
    )
    box = models.ForeignKey(Box, related_name="comics", on_delete=models.CASCADE)
    name = models.CharField("Title", max_length=120)
    slug = models.SlugField(unique=True)
    sImg = models.ImageField("Image", upload_to="comics/")
    number = models.PositiveSmallIntegerField()
    date = models.DateField()
    condition = models.CharField(
        max_length=100, choices=CONDITION_CHOICES, default=CON,
    )
    owned = models.BooleanField("I own this comic.", default=True)
    variant = models.CharField("Variant", max_length=5)
    owned = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


def create_box_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    query_set = Box.objects.filter(slug=slug)
    exists = query_set.exists()
    if exists:
        new_slug = "%s-%s" % (slug, uuid.uuid4().hex[:10])
        return create_box_slug(instance, new_slug=new_slug)
    return slug


def create_comic_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    query_set = Comic.objects.filter(slug=slug)
    exists = query_set.exists()
    if exists:
        new_slug = "%s-%s" % (slug, uuid.uuid4().hex[:10])
        return create_comic_slug(instance, new_slug=new_slug)
    return slug


# The presave will always be called before the save
def pre_save_receiver_box(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_box_slug(instance)


# The presave will always be called before the save
def pre_save_receiver_comic(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_comic_slug(instance)


pre_save.connect(pre_save_receiver_box, sender=Box)
pre_save.connect(pre_save_receiver_comic, sender=Comic)
