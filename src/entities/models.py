from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from PIL import Image
import os

def validate_image(image):
    """Validate that the file is an image."""
    valid_mime_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/webp']
    try:
        file_mime_type = Image.open(image).get_format_mimetype()
        if file_mime_type not in valid_mime_types:
            raise ValidationError(f'Invalid file type. Must be one of the following: {valid_mime_types}')
    except Exception as e:
        raise ValidationError('Error validating image file.')

def upload_to(instance, filename):
    return os.path.join(f'entities/images/{instance.pk or "unknown"}', filename)

class ImageWithCaption(models.Model):
    """Model to store images with captions."""
    image = models.ImageField(
        upload_to=upload_to,
        validators=[validate_image],
        help_text='Image file to upload.'
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Caption for the image.'
    )

    def __str__(self):
        return self.caption or 'No caption'

class Entity(models.Model):
    """Model to store entities."""
    ENTITY_TYPES_CHOICE = [
        ('Divinity', 'Divinity'),
        ('Hero', 'Hero'),
        ('Mythical Creature', 'Mythical Creature'),
    ]

    name = models.CharField(
        max_length=255,
        help_text='Name of the entity.'
    )
    entity_type = models.CharField(
        max_length=20,
        choices=ENTITY_TYPES_CHOICE,
        help_text='Type of entity.'
    )
    date_created = models.DateTimeField(auto_now_add=True, help_text='Date the entity was created.')
    date_modified = models.DateTimeField(auto_now=True, help_text='Date the entity was last modified.')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='User who created the entity.'
    )
    country_of_origin = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Country of origin of the entity.'
    )
    ethnicity = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Group of people the entity is associated with.'
    )
    gender = models.CharField(
        max_length=15,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Androgynous', 'Androgynous'),
            ('Spirit', 'Spirit'),
            ('Element', 'Element')
        ],
        blank=True,
        null=True,
        help_text='Gender of the entity.'
    )
    images = models.ManyToManyField(
        ImageWithCaption,
        blank=True,
        help_text='Images of the entity.'
    )

    class Meta:
        unique_together = ['name', 'entity_type']

    def __str__(self):
        return f"{self.name} ({self.get_entity_type_display()})"

class DivinityDetails(models.Model):
    entity = models.OneToOneField(
        Entity,
        on_delete=models.CASCADE,
        related_name='divinity_details',
        limit_choices_to={'entity_type': 'Divinity'}
    )
    cultural_role = models.CharField(
        max_length=100,
        help_text="Cultural role of the divinity, e.g., 'God of thunder'."
    )
    pantheon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="The pantheon to which the divinity belongs."
    )
    alignment = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Moral or ethical alignment of the divinity."
    )
    domains = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="Main domains associated with the divinity."
    )
    main_symbols = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="Main symbols associated with the divinity."
    )
    characteristics = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="Main traits or aspects of the mythological personality."
    )
    manifestations = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Descriptions of the forms the divinity can take in mythological accounts."
    )
    symbolic_animals = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="Animals symbolically linked to the divinity."
    )
    power_objects = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="Mythically significant objects associated with the divinity."
    )
    consorts = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="Name(s) of the divinity's consort(s) or partner(s), if applicable."
    )

    def __str__(self):
        return f"Details of divinity {self.entity.name}"

class HeroDetails(models.Model):
    entity = models.OneToOneField(
        Entity,
        on_delete=models.CASCADE,
        related_name='hero_details',
        limit_choices_to={'entity_type': 'Hero'}
    )
    titles = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Honorific titles or alternative names of the hero."
    )
    achievements = models.TextField(
        blank=True,
        null=True,
        help_text="Notable achievements or exploits of the hero."
    )
    enemies = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="Enemies or adversaries of the hero in myths."
    )
    allies = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="Allies or companions of the hero in myths."
    )

    def __str__(self):
        return f"Details of hero {self.entity.name}"

class MythicalCreatureDetails(models.Model):
    entity = models.OneToOneField(
        Entity,
        on_delete=models.CASCADE,
        related_name='creature_details',
        limit_choices_to={'entity_type': 'Mythical Creature'}
    )
    habitat = models.CharField(
        max_length=255,
        help_text="Natural or mythological habitat of the creature."
    )
    diet = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Diet of the mythical creature."
    )
    size = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Typical size or dimensions of the creature."
    )
    weaknesses = models.TextField(
        blank=True,
        null=True,
        help_text="Weaknesses or vulnerabilities of the creature."
    )
    strengths = models.TextField(
        blank=True,
        null=True,
        help_text="Strengths or special abilities of the creature."
    )

    def __str__(self):
        return f"Details of creature {self.entity.name}"
