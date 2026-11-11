from django.contrib import admin
from movies.models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":["category"]}

admin.site.register(Category,CategoryAdmin)