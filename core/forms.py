# core/forms.py
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PantryItem, Recipe, RecipeIngredient, ShoppingListItem, DocumentUpload, UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False)
    dietary_preferences = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "phone", "dietary_preferences", "password1", "password2")

class PantryItemForm(forms.ModelForm):
    class Meta:
        model = PantryItem
        fields = ["item_name", "quantity", "unit", "category", "expiry_date"]

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "category", "prep_time", "instructions"]

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ["name", "quantity_required", "unit"]

RecipeIngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=1, can_delete=True)

class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ["item_name", "quantity", "unit"]

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ["title", "file"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "dietary_preferences"]
