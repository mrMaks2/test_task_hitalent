from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Chat, Message

class ChatAPITestCase(APITestCase):
    
    def test_create_chat(self):
        """Тестирование создания нового чата"""
        url = reverse('chat-create')
        data = {'title': 'Test Chat'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(Chat.objects.get().title, 'Test Chat')
    
    def test_create_chat_empty_title(self):
        """Тестирование создания чата с пустым заголовком"""
        url = reverse('chat-create')
        data = {'title': ''}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_message(self):
        """Тестирование создания сообщения в чате"""
        chat = Chat.objects.create(title='Test Chat')
        url = reverse('message-create', kwargs={'chat_id': chat.id})
        data = {'text': 'Hello, world!'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().text, 'Hello, world!')
        self.assertEqual(Message.objects.get().chat.id, chat.id)
    
    def test_create_message_invalid_chat(self):
        """Тестирование создания сообщение в несуществующем чате"""
        url = reverse('message-create', kwargs={'chat_id': 999})
        data = {'text': 'Hello'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_chat_with_messages(self):
        """Тестирование получения чата с сообщениями"""
        chat = Chat.objects.create(title='Test Chat')
        Message.objects.create(chat=chat, text='Message 1')
        Message.objects.create(chat=chat, text='Message 2')
        
        url = reverse('chat-detail', kwargs={'pk': chat.id})
        response = self.client.get(url, {'limit': 10})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['messages']), 2)
    
    def test_delete_chat_cascades(self):
        """Тестирование, что удаление чата удаляет и сообщения"""
        chat = Chat.objects.create(title='Test Chat')
        Message.objects.create(chat=chat, text='Message 1')
        Message.objects.create(chat=chat, text='Message 2')
        
        self.assertEqual(Message.objects.count(), 2)
        
        url = reverse('chat-detail', kwargs={'pk': chat.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Chat.objects.count(), 0)
        self.assertEqual(Message.objects.count(), 0)


class ModelTestCase(TestCase):
    
    def test_chat_title_trimming(self):
        """Тестирование strip() для заголовка"""
        chat = Chat(title='  Test Chat  ')
        chat.save()
        self.assertEqual(chat.title, 'Test Chat')
    
    def test_message_text_trimming(self):
        """Тестирование strip() для текста"""
        chat = Chat.objects.create(title='Test Chat')
        message = Message(chat=chat, text='  Hello  ')
        message.save()
        self.assertEqual(message.text, 'Hello')