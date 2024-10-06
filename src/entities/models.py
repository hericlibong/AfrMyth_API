from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from PIL import Image
import os


def validate_image(image):
    """Validate the file is an image."""
    valid_mime_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/webp']
    try:
        file_mime_type = Image.open(image).get_format_mimetype()
        if file_mime_type not in valid_mime_types:
            raise ValidationError(f'Invalid file type. Must be one of the following: {valid_mime_types}')
    except Exception as e:
        raise ValidationError('Error validating image file.')
    
def upload_to(instance, filename):
    return os.path.join(f'entities/images/{instance.pk or "unknown"}', filename)


class ImageWitCaption(models.model):
    """Model to store images with captions."""
    image = models.ImageField(
        upload_to=upload_to,
        blank=True,
        null=True,
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
        ('Hero', 'Hero')
        ('Mythical Creature', 'Mythical Creature'),
    ]

    name = models.CharField(
        max_length=255,
        help_text='Name of the entity.'
        )
    entity_type = models.CharField(max_length=255, choices=ENTITY_TYPES_CHOICE, help_text='Type of entity.')
    date_created = models.DateTimeField(auto_now_add=True, help_text='Date the entity was created.')
    date_modified = models.DateTimeField(auto_now=True, help_text='Date the entity was last modified.')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
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
        help_text= "Group of people the entity is associated with."
        )
    gender = models.CharField(
        max_length=10,
        choices = [('Male', 'Male'), ('Female', 'Female'), ('Androgyn', 'Androgyn'), 
                   ('Spirit', 'Spirit'), ('Element', 'Element') ],
        blank=True,
        null=True,
        help_text="Gender of the entity.")
    parents = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text='Parents of the entity.'
        )
    descendants = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text='Descendants of the entity.'
        )
    appearance = models.TextField(
        blank=True,
        null=True,
        help_text='Physical appearance of the entity.'
        )
    story = models.TextField(
        blank=True,
        null=True,
        help_text='Story or legends about the entity.'
        )
    powers = models.TextField(
        blank=True,
        null=True,
        help_text='Powers or extraordinaries capacities of the entity.'
        )
    images = models.ManyToManyField(
        ImageWitCaption,
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
        help_text="Rôle culturel de la divinité, par exemple 'Dieu du tonnerre'."
    )
    pantheon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Le panthéon auquel appartient la divinité."
    )
    alignment = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Alignement moral ou éthique de la divinité."
    )
    domain = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text="Domaines principaux associés à la divinité."
    )
    main_symbol = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text="Symboles principaux associés à la divinité."
    )
    characteristics = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text="Traits principaux ou aspects de la personnalité mythique."
    )
    manifestations = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Descriptions des formes que la divinité peut prendre dans les récits mythologiques."
    )
    symbolic_animals = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text="Animaux symboliquement liés à la divinité."
    )
    power_objects = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text="Objets mythiquement significatifs associés à la divinité."
    )
    conjoint = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text="Nom du conjoint ou partenaire de la divinité, si applicable."
    )

    def __str__(self):
        return f"Détails de la divinité {self.entity.name}"

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
        help_text="Titres honorifiques ou noms alternatifs du héros."
    )
    achievements = models.TextField(
        blank=True,
        null=True,
        help_text="Réalisations notables ou exploits du héros."
    )
    enemies = models.TextField(
        blank=True,
        null=True,
        help_text="Ennemis ou adversaires du héros dans les mythes."
    )
    allies = models.TextField(
        blank=True,
        null=True,
        help_text="Alliés ou compagnons du héros dans les mythes."
    )

    def __str__(self):
        return f"Détails du héros {self.entity.name}"

class MythicalCreatureDetails(models.Model):
    entity = models.OneToOneField(
        Entity,
        on_delete=models.CASCADE,
        related_name='creature_details',
        limit_choices_to={'entity_type': 'Creature'}
    )
    habitat = models.CharField(
        max_length=255,
        help_text="Habitat naturel ou mythologique de la créature."
    )
    diet = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Régime alimentaire de la créature mythique."
    )
    size = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Taille ou dimensions typiques de la créature."
    )
    weaknesses = models.TextField(
        blank=True,
        null=True,
        help_text="Faiblesses ou vulnérabilités de la créature."
    )
    strengths = models.TextField(
        blank=True,
        null=True,
        help_text="Forces ou capacités spéciales de la créature."
    )

    def __str__(self):
        return f"Détails de la créature {self.entity.name}"
    
    
    