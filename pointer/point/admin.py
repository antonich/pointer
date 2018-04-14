from django.contrib import admin

from point.models import Pointer, PublicPointer, PrivatePointer
# Register your models here.

class PointerAdmin(admin.ModelAdmin):
    fields = ('title', 'author')


class PublicPointerAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'is_private')

class PrivatePointerAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'is_private')

admin.site.register(Pointer, PointerAdmin)
admin.site.register(PublicPointer, PublicPointerAdmin)
admin.site.register(PrivatePointer, PrivatePointerAdmin)
