from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address

class AddressInline(admin.StackedInline):
    model = Address
    extra = 1  # Number of blank forms to display for new addresses
    fields = ('address_type', 'address_line_1', 'address_line_2', 'city', 'province', 'postal_code', 'country')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [AddressInline]  # Add the AddressInline
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'is_temporary', 'role')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

    # list_filter = ('is_staff', 'is_active', 'groups')
    # ordering = ('-date_joined',)

    # 如果有自定义字段，可以使用 `fieldsets` 来控制显示
    # fieldsets = UserAdmin.fieldsets + (
    #     ('Custom Fields', {'fields': ('your_custom_field',)}),
    # )
