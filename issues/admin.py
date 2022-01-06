from django.contrib import admin
from issues.models import Issue
from import_export.admin import ImportExportModelAdmin


class IssueAdmin(ImportExportModelAdmin):
    list_display = (
        "creation_date",
        "name",
        "status",
        "project",
        "reported_by",
        "assigned_to",
    )
    ordering = ("-creation_date", "name", )     # '-' means descending
    search_fields = ("name", "description", )
    filter_horizontal = ("linked_issues",)

    # CURTIS - hide state value used to trigger logic on saving issue changes
    exclude = ('state', 'linked_issues',)

    # CURTIS: Override get_queryset to get only issues associated with user's projects
    def get_queryset(self, request):
        # Start with full queryset
        queryset = super().get_queryset(request)
        # Filter based on the project (from queryset) being among those associated with user
        queryset = queryset.filter(project__in=request.user.projects.all())
        return queryset


admin.site.register(Issue, IssueAdmin)
