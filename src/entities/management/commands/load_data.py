from django.core.management.base import BaseCommand
from entities.models import Entity, DivinityDetails, HeroDetails, MythicalCreatureDetails
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class Command(BaseCommand):
    """ Load data from Json File to the database """
    help = 'Load data from Json File to the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Json File to load data from')
        parser.add_argument('--user', type=str, help='User that create the entity')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        username = kwargs['user']

        created_by = None
        if username:
            try:
                created_by = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))
                return

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{json_file}" not found.'))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Error decoding JSON: {e}'))
            return

        for entity in data:
            try:
                # Validation du type d'entité
                entity_type = entity.get('entity_type')
                if entity_type not in ['Divinity', 'Hero', 'Mythical Creature']:
                    self.stdout.write(self.style.WARNING(f"Invalid entity_type '{entity_type}' for entity '{entity.get('name', 'Unknown')}'. Skipping."))
                    continue

                # Création de l'entité
                entity_obj = Entity.objects.create(
                    name=entity['name'],
                    entity_type=entity_type,
                    created_by=created_by,
                    country_of_origin=entity.get('country_of_origin'),
                    ethnicity=entity.get('ethnicity'),
                    gender=entity.get('gender'),
                )
                self.stdout.write(f"Created entity '{entity_obj.name}' of type '{entity_obj.entity_type}'.")

                # Création des détails spécifiques
                if entity_type == 'Divinity':
                    DivinityDetails.objects.create(
                        entity=entity_obj,
                        cultural_role=entity.get('cultural_role'),
                        pantheon=entity.get('pantheon'),
                        alignment=entity.get('alignment'),
                        domains=entity.get('domains', []),
                        main_symbols=entity.get('main_symbols', []),
                        characteristics=entity.get('characteristics', []),
                        manifestations=entity.get('manifestations'),
                        symbolic_animals=entity.get('symbolic_animals', []),
                        power_objects=entity.get('power_objects', []),
                        consorts=entity.get('consorts', []),
                    )
                    self.stdout.write(self.style.SUCCESS(f"Divinity details for '{entity_obj.name}' created successfully."))

                elif entity_type == 'Hero':
                    HeroDetails.objects.create(
                        entity=entity_obj,
                        titles=entity.get('titles'),
                        achievements=entity.get('achievements'),
                        enemies=entity.get('enemies', []),
                        allies=entity.get('allies', []),
                    )
                    self.stdout.write(self.style.SUCCESS(f"Hero details for '{entity_obj.name}' created successfully."))

                elif entity_type == 'Mythical Creature':
                    MythicalCreatureDetails.objects.create(
                        entity=entity_obj,
                        habitat=entity.get('habitat'),
                        diet=entity.get('diet'),
                        size=entity.get('size'),
                        weaknesses=entity.get('weaknesses'),
                        strengths=entity.get('strengths'),
                    )
                    self.stdout.write(self.style.SUCCESS(f"Mythical creature details for '{entity_obj.name}' created successfully."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating entity '{entity.get('name', 'Unknown')}': {e}"))
                continue  # Passer à l'entité suivante en cas d'erreur
