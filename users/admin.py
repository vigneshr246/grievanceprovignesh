from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, GrievanceCategory, Grievance, GrievanceAttachment, Feedback, Report


# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "name", "phone", "role", "is_admin"]
    list_filter = ["is_admin", "role"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name", "phone", "role"]}),
        ("Permissions", {"fields": ["is_admin", "is_active", "is_superuser", "groups", "user_permissions"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "phone", "role", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "name", "phone"]
    ordering = ["email"]
    filter_horizontal = ["groups", "user_permissions"]


class GrievanceCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name", "description"]


class GrievanceAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "status", "priority", "department", "created_at", "updated_at"]
    list_filter = ["status", "priority", "department"]
    search_fields = ["title", "description", "user__email"]


class GrievanceAttachmentAdmin(admin.ModelAdmin):
    list_display = ["grievance", "file", "uploaded_at"]
    search_fields = ["grievance__title"]


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["grievance", "user", "rating", "created_at"]
    search_fields = ["grievance__title", "user__email", "comments"]


class ReportAdmin(admin.ModelAdmin):
    list_display = ["start_date", "end_date", "created_at", "grievance_count", "resolved_count", "escalated_count", "average_resolution_time"]
    search_fields = ["start_date", "end_date"]


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(GrievanceCategory, GrievanceCategoryAdmin)
admin.site.register(Grievance, GrievanceAdmin)
admin.site.register(GrievanceAttachment, GrievanceAttachmentAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Report, ReportAdmin)


# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

