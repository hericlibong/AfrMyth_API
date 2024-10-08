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
                self.stdout.write(self.style.ERROR(f'User {username} does not exist.'))
                return
        
        with open(json_file) as f:
            data = json.load(f)
            for entity in data:
                entity_obj = Entity.objects.create(
                    name=entity['name'],
                    entity_type=entity['entity_type'],
                    created_by=created_by
                )
                if entity['entity_type'] == 'Divinity':
                    DivinityDetails.objects.create(
                        entity=entity_obj,
                        domain=entity['domain'],
                        pantheon=entity['pantheon']
                    )
                elif entity['entity_type'] == 'Hero':
                    HeroDetails.objects.create(
                        entity=entity_obj,
                        superpowers=entity['superpowers'],
                        weaknesses=entity['weaknesses']
                    )
                elif entity['entity_type'] == 'Mythical Creature':
                    MythicalCreatureDetails.objects.create(
                        entity=entity_obj,
                        habitat=entity['habitat'],
                        diet=entity['diet']
                    )

