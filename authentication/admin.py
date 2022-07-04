from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import User
from manageshape.models import Shape

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Shape)
