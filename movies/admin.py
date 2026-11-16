from django.contrib import admin
from movies.models import Category,Movie,Cast

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":["category"]}

admin.site.register(Category,CategoryAdmin)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    filter_horizontal=("actors")
    list_filter = ("actors")

