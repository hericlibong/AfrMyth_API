from django.contrib import admin
from .models import Entity, ImageWithCaption, DivinityDetails, HeroDetails, MythicalCreatureDetails

admin.site.register(Entity)
admin.site.register(ImageWithCaption)
admin.site.register(DivinityDetails)
admin.site.register(HeroDetails)
admin.site.register(MythicalCreatureDetails)
