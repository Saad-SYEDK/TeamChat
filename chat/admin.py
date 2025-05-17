from django.contrib import admin
from .models import Chat, Message

class CustomAdminSite(admin.AdminSite):
    site_header = 'Real-Time Chat Admin'
    site_title = 'Chat Admin'
    index_title = 'Welcome to Chat Admin Panel'

    def each_context(self, request):
        context = super().each_context(request)
        context['css_files'] = ['chat/admin.css']
        return context

admin_site = CustomAdminSite(name='custom_admin')

admin_site.register(Chat)
admin_site.register(Message)
