from django.contrib import admin
from .models import Entity, ImageWithCaption, DivinityDetails, HeroDetails, MythicalCreatureDetails

class ImageWithCaptionInline(admin.TabularInline):
    model = Entity.images.through
    extra = 1

class DivinityDetailsInline(admin.StackedInline):
    model = DivinityDetails
    extra = 1

class HeroDetailsInline(admin.StackedInline):
    model = HeroDetails
    extra = 1

class MythicalCreatureDetailsInline(admin.StackedInline):
    model = MythicalCreatureDetails
    extra = 1

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    inlines = [
        ImageWithCaptionInline,
        DivinityDetailsInline,
        HeroDetailsInline,
        MythicalCreatureDetailsInline
    ]
    list_display = ['name', 'entity_type']
    list_filter = ['entity_type']
    search_fields = ['name']
    readonly_fields = ['date_created', 'date_modified']
    fieldsets = [
        (None, {'fields': ['name', 'entity_type']}),
        ('Description', {'fields': ['country_of_origin', 'ethnicity', 'gender']}),
        ('Author', {'fields': ['created_by']}),
        ('dates', {'fields': ['date_created', 'date_modified']})
    ]


admin.site.register(ImageWithCaption)
# admin.site.register(DivinityDetails)
# admin.site.register(HeroDetails)
# admin.site.register(MythicalCreatureDetails)


