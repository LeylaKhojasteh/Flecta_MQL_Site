from django.contrib import admin

from website.models import Contact, Newsletter

# Register your models here.




class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_date')
    list_filter = ('email',)
    search_fields = ('name', 'email', 'subject', 'message')


admin.site.register(Contact, ContactAdmin)
admin.site.register(Newsletter)