from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = (
        "name",
        "used_by"
    )

    def used_by(self, obj):
        return obj.rooms.count()

    pass

class PhotoInline(admin.TabularInline):

    model = models.Photo

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "More About the Space",
            {"classes": ('collapse',), "fields": ("amenities", "facilities", "house_rules")},
        ),
        (
            "Spaces",
            {"fields": ("guests", "beds", "bedrooms", "baths")},
        ),
        (
            "List Details",
            {"fields": ("host",)},
        ),
    )

    ordering = ("name", "price", "bedrooms")

    list_display = (
        "name",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "room_type",
        "host__gender",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)

    search_fields = ("city", "host__username")

    filter_horizontal = ("amenities", "facilities", "house_rules",)

    def save_model(self, request, obj, form, change):
        print(obj, change, form)
        super().save_model(request, obj, form, change)

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "amenities numbers"

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ('__str__', 'get_thumbnail')

    def get_thumbnail(self, obj):
        print(obj.file.url)
        return f'<img src="{obj.file.url}" />'

    get_thumbnail.short_description = "Thumbnail"

