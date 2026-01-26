from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Prefetch
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, ChatDetailSerializer
import logging

logger = logging.getLogger(__name__)


class ChatCreateView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Создание нового чата с заголовком: {request.data.get('title')}")
        return super().create(request, *args, **kwargs)


class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['chat_id'] = self.kwargs['chat_id']
        return context
    
    def create(self, request, *args, **kwargs):
        chat_id = self.kwargs['chat_id']
        
        chat = get_object_or_404(Chat, id=chat_id)
        
        logger.info(f"Создание сообщения в чате {chat_id}")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message = serializer.save(chat=chat)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ChatDetailView(generics.RetrieveDestroyAPIView):
    queryset = Chat.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ChatDetailSerializer
        return ChatSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.request.method == 'GET':
            # Для GET-запросов используем выборку сообщений.
            limit = min(int(self.request.query_params.get('limit', 20)), 100)
            queryset = queryset.prefetch_related(
                models.Prefetch(
                    'messages',
                    queryset=Message.objects.all().order_by('-created_at')[:limit]
                )
            )
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Получение чата {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Удаление чата {instance.id} со всеми сообщениями")
        return super().destroy(request, *args, **kwargs)