# core/admin.py
from django.contrib import admin
from .models import (
    UserProfile, PantryItem, Recipe, RecipeIngredient,
    IngredientSubstitution, ShoppingListItem, DocumentUpload
)

admin.site.register(UserProfile)
admin.site.register(PantryItem)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(IngredientSubstitution)
admin.site.register(ShoppingListItem)
admin.site.register(DocumentUpload)
