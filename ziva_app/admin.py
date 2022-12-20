from django.contrib import admin

# Register your models here.
from .models import UOM,Region,Category

admin.site.register(UOM)

admin.site.register(Region)

admin.site.register(Category)
