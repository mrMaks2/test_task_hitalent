from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['title']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat', 'text_preview', 'created_at']
    list_filter = ['created_at', 'chat']
    search_fields = ['text', 'chat__title']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'