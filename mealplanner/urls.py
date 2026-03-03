from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", core_views.home, name="home"),  # actual dashboard now at /home/

    # authentication
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),  # 🔹 fixed

    # signup
    path("signup/", core_views.signup_view, name="signup"),

    # app pages
    path("", core_views.home, name="entry"),   # ✅ dashboard
    path("pantry/", core_views.pantry_list, name="pantry_list"),
    path("pantry/<int:pk>/edit/", core_views.pantry_edit, name="pantry_edit"),
    path("pantry/<int:pk>/delete/", core_views.pantry_delete, name="pantry_delete"),
    path("recipes/", core_views.recipe_list, name="recipe_list"),
    path("recipes/add/", core_views.recipe_create, name="recipe_create"),
    path("recipes/<int:pk>/", core_views.recipe_detail, name="recipe_detail"),
    path("recipes/<int:pk>/edit/", core_views.recipe_edit, name="recipe_edit"),
    path("recipes/<int:pk>/delete/", core_views.recipe_delete, name="recipe_delete"),

    path("shopping/", core_views.shopping_list, name="shopping_list"),
    path("shopping/<int:pk>/mark/", core_views.mark_bought, name="mark_bought"),
    path("upload/", core_views.document_upload, name="document_upload"),

    # suggestions API
    path("api/suggestions/", core_views.suggestions_api, name="api_suggestions"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
