from django.contrib import admin
from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {
            'fields': ('username', ),
            'classes': ('wide', 'extrapretty'),
        }),
        ('基本信息', {
            'fields': (('first_name', 'last_name'), ('email', 'phone_number'),
                       'password', ('date_joined', 'last_login')),
            'classes': ('wide', 'extrapretty'),
        }),
        ('等级权限', {
            'fields': (('is_superuser', 'is_staff', 'is_active'), ),
        }),
    ]
    list_display = ('id', 'username', 'email', 'phone_number', 'date_joined', 'last_login', 'is_superuser')
    list_display_links = ('id', 'username', 'email', 'phone_number')
    list_filter = ('date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active')
    search_fields = ['username', 'email', 'phone_number']

admin.site.register(User, UserAdmin)
