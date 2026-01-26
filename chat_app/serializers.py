from rest_framework import serializers
from .models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'title', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Заголовок не может быть пустым.")
        if len(value) > 200:
            raise serializers.ValidationError("Заголовок не может превышать 200 символов.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_text(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Текст не может быть пустым.")
        if len(value) > 5000:
            raise serializers.ValidationError("Текст не может превышать 5000 символов.")
        return value


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'title', 'created_at', 'updated_at', 'messages']