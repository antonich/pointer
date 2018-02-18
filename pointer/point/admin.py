from django.contrib import admin

from point.models import Pointer, PublicPointer, PrivatePointer
# Register your models here.

class PointerAdmin(admin.ModelAdmin):
    fields = ('title', 'author')

admin.site.register(Pointer)
