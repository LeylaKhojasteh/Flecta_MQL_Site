from django.contrib import admin

from website.models import Contact

# Register your models here.




class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'project_type','platform','subject', 'created_date')
    list_filter = ('project_type','platform','created_date',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_date','updated_date',)

admin.site.register(Contact, ContactAdmin)
