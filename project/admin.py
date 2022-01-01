from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project


class ProjectAdmin(admin.ModelAdmin):
    fields = ("name", "active")


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
