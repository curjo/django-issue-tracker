from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'YoJonesy project data',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'is_designer',
                    'is_developer',
                    'projects',
                ),
            },
        ),
    )


class ProjectAdmin(admin.ModelAdmin):
    fields = ("name", "active")


#admin.site.register(User, UserAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Project, ProjectAdmin)
