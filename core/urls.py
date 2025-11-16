from django.urls import path
from . import views

urlpatterns = [
    # Эндпоинты Вопросов
    path('questions/', views.QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    
    # Эндпоинты Ответов
    path('questions/<int:question_id>/answers/', views.AnswerCreateView.as_view(), name='answer-create'),
    path('answers/<int:pk>/', views.AnswerDetailView.as_view(), name='answer-detail'),
]