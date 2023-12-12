from django.contrib import admin
from django.utils.html import format_html

from .models import *



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name", "image")

admin.site.register(User)
# @admin.register(User)
# class CategoryAdmin(admin.ModelAdmin):
#     search_fields = ["login","password"]
#     list_display = ("name", "image")
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ["name", 'text']
    list_display = ("name", "title","text")


    def custom_display(self, obj):
        # Corrected: Accessing 'slug' attribute from the 'obj' parameter
        if not obj.slug:
            return "No Slug"
        return obj.slug

    custom_display.short_description = "Custom Display"

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ("name" , "title" , "image", "salary", "vaqti", "text", "desc", "status")


    def some_method(self, obj):
        # Corrected: Implement the 'some_method' logic based on your model
        return "Your Implementation Here"  # Replace with the actual implementation

    some_method.short_description = "Some Method"

# Unregister the Work model first before registering it with WorkAdmin
