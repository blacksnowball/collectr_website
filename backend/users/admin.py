"""
A default admin file from django
"""
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.contrib import admin
from rest_framework_simplejwt import token_blacklist
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from .models import CustomUser

class UserAdminConfig(UserAdmin):
    """
    A class for the configuration of admin panel for users
    """
    model = CustomUser
    search_fields = ('email', 'username')
    list_filter = ('email', 'username', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'username', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about', 'picture')}),
    )
    formfield_overrides = {
        CustomUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )

admin.site.register(CustomUser, UserAdminConfig)

class OutstandingTokenAdmin(OutstandingTokenAdmin):
    """
    A class for representing admin token
    """
    def has_delete_permission(self, *args, **kwargs):
        """
        A method for checking whether or not someone has
        delete permission
        """
        return True

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)
