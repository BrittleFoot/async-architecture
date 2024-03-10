from django.contrib import admin

from users.models import User, UserRole


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
