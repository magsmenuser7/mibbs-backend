from django.contrib import admin
from .models import Users, Role, UserRole
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Users)
class UsersAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'role', 'is_active', 'is_superuser', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('is_active', 'is_superuser', 'is_staff', 'role')

@admin.register(Role)
class RoleAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'role_name', 'role_category', 'created_at')
    search_fields = ('role_name',)

@admin.register(UserRole)
class UserRoleAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'user', 'role', 'created_by', 'created_at')
    search_fields = ('user__username', 'role__role_name')

