# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    dietary_preferences = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class PantryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pantry_items")
    item_name = models.CharField(max_length=200)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=30, blank=True)
    category = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.item_name} ({self.quantity} {self.unit})"

class Recipe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    prep_time = models.PositiveIntegerField(default=15)
    instructions = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=200)
    quantity_required = models.FloatField(default=1)
    unit = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} for {self.recipe.name}"

class IngredientSubstitution(models.Model):
    ingredient = models.CharField(max_length=200, unique=True)
    substitutes = models.JSONField(default=list, blank=True)  # e.g. ["almond milk", "soy milk"]

    def __str__(self):
        return self.ingredient

class ShoppingListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shopping_items")
    item_name = models.CharField(max_length=200)
    quantity = models.FloatField(default=1)
    unit = models.CharField(max_length=30, blank=True)
    purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item_name} ({'bought' if self.purchased else 'pending'})"

class DocumentUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to="documents/%Y/%m/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.file.name
