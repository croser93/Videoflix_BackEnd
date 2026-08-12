from django.contrib import admin
from auth_app.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class OffersAdmin(admin.ModelAdmin):
    list_display = ['id','username','email']