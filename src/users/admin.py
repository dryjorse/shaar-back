from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
  model = User
  list_display = ('email', 'username')
  list_filter = ('is_staff', 'is_active')
  search_fields = ('email', 'username',)
  ordering = ('email',)
  filter_horizontal = ()

  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Personal info', {'fields': ('username','ava')}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    ('Important dates', {'fields': ('last_login', 'date_joined')}),
  )

  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'username', 'password1', 'password2')}
    ),
  )

admin.site.register(User, UserAdmin)