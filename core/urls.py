# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard is routed at project level to '/', but keep name
    path("pantry/", views.pantry_list, name="pantry_list"),
    path("pantry/<int:pk>/edit/", views.pantry_edit, name="pantry_edit"),
    path("pantry/<int:pk>/delete/", views.pantry_delete, name="pantry_delete"),

    path("recipes/", views.recipe_list, name="recipe_list"),
    path("recipes/add/", views.recipe_create, name="recipe_create"),
    path("recipes/<int:pk>/", views.recipe_detail, name="recipe_details"),
    path("recipes/<int:pk>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipes/<int:pk>/delete/", views.recipe_delete, name="recipe_delete"),
    # inside urlpatterns - add:
    

    path("shopping/", views.shopping_list, name="shopping_list"),
    path("shopping/add/", views.shopping_add, name="shopping_add"),
    path("shopping/<int:pk>/bought/", views.mark_bought, name="mark_bought"),

    path("profile/", views.profile_edit, name="profile_edit"),
    path("upload-doc/", views.upload_doc, name="upload_doc"),

    path("api/suggestions/", views.suggestions_api, name="api_suggestions"),
]

