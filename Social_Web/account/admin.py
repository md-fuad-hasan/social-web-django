from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import SocialUser,UserProfile

# Register your models here.


class SocialUserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = ["email", "roll","username", "is_superuser", "is_staff", "is_active"]
    list_filter = ["is_superuser"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["roll","username"]}),
        ("Permissions", {"fields": ["is_superuser","is_staff","is_active"]}),
        ('Group Permissions', {
            
            'fields': ('groups','user_permissions', )
        })
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "roll","username","password1", "password2"],
            },
        ),
    ]
    search_fields = ["email","roll","username"]
    ordering = ["id","roll","username"]
    filter_horizontal = []


admin.site.register(SocialUser,SocialUserAdmin)
admin.site.register(UserProfile)