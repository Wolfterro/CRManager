from django.contrib import admin

from user.models import UserProfile, Address


# Register your models here.
# ==========================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    def city_and_uf(self, obj):
        return obj.city_and_uf()
    city_and_uf.short_description = 'Cidade e Estado'

    def user_cr(self, obj):
        return obj.cr_set.first()
    user_cr.short_description = 'CR'

    list_display = ('full_name', 'email', 'cpf', 'rg', 'birthday', 'city_and_uf', 'user_cr', )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
