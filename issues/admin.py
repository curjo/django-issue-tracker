from django.contrib import admin
from issues.models import Issue
from import_export.admin import ImportExportModelAdmin


class IssueAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "status",
        "project",
        "reported_by",
        "assigned_to",
    )
    ordering = ("project", "name", )
    search_fields = ("name", "description", )
    filter_horizontal = ("linked_issues",)

    # CURTIS - hide state value used to trigger logic on saving issue changes
    exclude = ('state',)


admin.site.register(Issue, IssueAdmin)
