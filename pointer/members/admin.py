from django.contrib import admin

from members.models import Member
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    fields = ('user', 'pointer', 'status')


admin.site.register(Member, MemberAdmin)
