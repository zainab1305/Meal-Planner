# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import (
    PantryItem, Recipe, RecipeIngredient,
    IngredientSubstitution, ShoppingListItem, DocumentUpload
)
from .forms import (
    SignUpForm, PantryItemForm, RecipeForm,
    RecipeIngredientFormSet, ShoppingListForm,
    DocumentUploadForm, UserProfileForm
)


# ENTRY: always show login page first (logs out any existing user)
def entry(request):
    # If someone is logged in, log them out so they always see login page first.
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = user.userprofile
            profile.phone = form.cleaned_data.get("phone")
            profile.dietary_preferences = form.cleaned_data.get("dietary_preferences")
            profile.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def home(request):
    pantry_count = PantryItem.objects.filter(user=request.user).count()
    recipe_count = Recipe.objects.filter(owner=request.user).count()
    shopping_count = ShoppingListItem.objects.filter(user=request.user).count()
    expiring = PantryItem.objects.filter(user=request.user, expiry_date__isnull=False).order_by("expiry_date")[:5]

    return render(request, "core/home.html", {
        "pantry_count": pantry_count,
        "recipe_count": recipe_count,
        "shopping_count": shopping_count,
        "expiring": expiring,
    })


# Pantry CRUD (unchanged)
@login_required
def pantry_list(request):
    if request.method == "POST":
        form = PantryItemForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            return redirect("pantry_list")
    else:
        form = PantryItemForm()
    pantry_items = PantryItem.objects.filter(user=request.user).order_by("item_name")
    return render(request, "core/pantry_list.html", {"form": form, "pantry_items": pantry_items})


@login_required
def pantry_edit(request, pk):
    item = get_object_or_404(PantryItem, pk=pk, user=request.user)
    if request.method == "POST":
        form = PantryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("pantry_list")
    else:
        form = PantryItemForm(instance=item)
    return render(request, "core/pantry_form.html", {"form": form})


@login_required
def pantry_delete(request, pk):
    item = get_object_or_404(PantryItem, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect("pantry_list")
    return render(request, "core/pantry_delete.html", {"item": item})


# Recipes: list / create / edit / delete / detail view
@login_required
def recipe_list(request):
    # show user's recipes + public ones
    recipes = (Recipe.objects.filter(owner=request.user) | Recipe.objects.filter(is_public=True)).distinct()
    return render(request, "core/recipe_list.html", {"recipes": recipes})

@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.save()

            # ✅ bind the instance properly here
            formset = RecipeIngredientFormSet(request.POST, instance=recipe)
            if formset.is_valid():
                formset.save()
                return redirect("recipe_list")
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    return render(request, "core/recipe_form.html", {"form": form, "formset": formset})

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, instance=recipe)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("recipe_list")
    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(instance=recipe)
    return render(request, "core/recipe_form.html", {"form": form, "formset": formset, "edit": True})


@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    if request.method == "POST":
        recipe.delete()
        return redirect("recipe_list")
    return render(request, "core/recipe_delete.html", {"recipe": recipe})
# New: view-only recipe detail (safe alternative to edit)
@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, owner=request.user)
    ingredients = recipe.ingredients.all()  # 🔹 get ALL related ingredients
    return render(request, "core/recipe_detail.html", {
        "recipe": recipe,
        "ingredients": ingredients,
    })



# Shopping list
@login_required
def shopping_list(request):
    if request.method == "POST":
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.user = request.user
            s.save()
            return redirect("shopping_list")
    else:
        form = ShoppingListForm()
    items = ShoppingListItem.objects.filter(user=request.user)
    return render(request, "core/shopping_list.html", {"form": form, "items": items})


@login_required
def mark_bought(request, pk):
    item = get_object_or_404(ShoppingListItem, pk=pk, user=request.user)
    item.purchased = True
    item.save()

    # update pantry correctly
    pantry, created = PantryItem.objects.get_or_create(
        user=request.user,
        item_name=item.item_name,   # ✅ correct field
        defaults={"quantity": 0, "unit": item.unit or ""}
    )
    pantry.quantity = (pantry.quantity or 0) + item.quantity
    pantry.save()

    return redirect("shopping_list")



# Documents (unchanged)
@login_required
def document_upload(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            return redirect("document_upload")
    else:
        form = DocumentUploadForm()
    docs = DocumentUpload.objects.filter(user=request.user).order_by("-uploaded_at")
    return render(request, "core/document_upload.html", {"form": form, "docs": docs})


# Suggestions API — checks ALL ingredients properly
@login_required
def suggestions_api(request):
    def normalize(s): return (s or "").strip().lower()

    # Build pantry mapping: name -> PantryItem
    pantry_qs = PantryItem.objects.filter(user=request.user)
    pantry = {normalize(p.item_name): p for p in pantry_qs}

    results = []
    # consider user's recipes and public ones
    recipes_qs = (Recipe.objects.filter(owner=request.user) | Recipe.objects.filter(is_public=True)).distinct()

    for recipe in recipes_qs:
        ingredients = list(recipe.ingredients.all())
        total = len(ingredients) if ingredients else 1
        matched = 0
        missing = []
        substitutions = {}

        for ing in ingredients:
            ing_name = normalize(getattr(ing, "ingredient", None) or getattr(ing, "name", None) or "")
            try:
                req_qty = float(getattr(ing, "quantity", None) or getattr(ing, "quantity_required", None) or 1)
            except Exception:
                req_qty = 1


            pantry_item = pantry.get(ing_name)
            if pantry_item:
                try:
                    have_qty = float(pantry_item.quantity or 0)
                except Exception:
                    have_qty = 0
            else:
                have_qty = 0

            if pantry_item and have_qty >= req_qty:
                matched += 1
            else:
                missing.append({"name": getattr(ing, "name", None) or getattr(ing, "ingredient", None),
                                "qty": req_qty,
                                "unit": getattr(ing, "unit", "")})
                # check substitution table
                try:
                    sub = IngredientSubstitution.objects.get(ingredient__iexact=ing_name)
                    have = [s for s in sub.substitutes if normalize(s) in pantry]
                    if have:
                        substitutions[ing.name if hasattr(ing, "name") else ing.ingredient] = have
                except IngredientSubstitution.DoesNotExist:
                    pass

        score = matched / total
        print("Recipe:", recipe.name, "Missing:", missing)
        results.append({
            "id": recipe.id,
            "name": recipe.name,
            "score": round(score, 2),
            "missing": missing,
            "substitutions": substitutions,
            "total_ingredients": total
        })

    # Sort primarily by score desc, then fewer missing
    results.sort(key=lambda r: (r["score"], -len(r["missing"])), reverse=True)
    return JsonResponse({"results": results})
