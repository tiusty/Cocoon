from django.contrib import admin
from cocoon.userAuth.forms import BaseRegisterForm
from .models import MyUser
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile


class UserAdmin(BaseUserAdmin):
    # Form to add a user
    add_form = BaseRegisterForm
    readonly_fields = ("joined",)
    # The fields to be used in displaying the User model:
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    list_display = ('email', 'joined', 'first_name', 'last_name', 'is_admin', 'is_hunter', 'is_broker')
    list_filter = ('is_admin', 'is_hunter', 'is_broker',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Joined', {'fields': ('joined',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_hunter', 'is_broker')}),
    )
    # add_fields sets is not a standard ModelAdmin Attribute. UserAdmin
    # overrides get_fieldsset to use this attirbute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'joined', 'first_name', 'last_name', 'password1', 'password2', 'creation_key')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class ProfileInline(admin.StackedInline):
    raw_id_fields = ("favorites", "visit_list",)
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.register(MyUser, CustomUserAdmin)
admin.site.unregister(Group)