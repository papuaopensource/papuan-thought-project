from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import User, Profile, Invitation
from . import services


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("username", "email", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff")
    search_fields = ("username", "email")
    actions = ["approve_users"]

    def save_model(self, request, obj, form, change):
        if change:
            try:
                was_inactive = not User.objects.filter(pk=obj.pk, is_active=True).exists()
            except Exception:
                was_inactive = False
            super().save_model(request, obj, form, change)
            if was_inactive and obj.is_active:
                services.send_approval_email(obj, request)
        else:
            super().save_model(request, obj, form, change)

    @admin.action(description="Approve selected users")
    def approve_users(self, request, queryset):
        approved = 0
        for user in queryset.filter(is_active=False):
            services.approve_user(user, request)
            approved += 1
        if approved:
            self.message_user(request, f"{approved} account(s) approved and notification email(s) sent.", messages.SUCCESS)
        else:
            self.message_user(request, "No pending accounts were selected.", messages.WARNING)


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "location", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("motivation",)
    raw_id_fields = ("user",)


@admin.register(Invitation)
class InvitationAdmin(ModelAdmin):
    list_display = ("email", "invited_by", "created_at", "is_used_display")
    readonly_fields = ("token", "created_at", "used_at", "invited_by")
    search_fields = ("email",)

    def is_used_display(self, obj):
        return obj.is_used
    is_used_display.boolean = True
    is_used_display.short_description = "Used"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.invited_by = request.user
            super().save_model(request, obj, form, change)
            try:
                services.create_invitation(obj.email, request.user, request)
            except ValueError as e:
                self.message_user(request, str(e), messages.ERROR)
        else:
            super().save_model(request, obj, form, change)
