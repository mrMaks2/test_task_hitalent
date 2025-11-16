from logging_utils import setup_logger
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Question, Answer
from .serializers import (
    QuestionSerializer, 
    CreateQuestionSerializer,
    AnswerSerializer, 
    CreateAnswerSerializer
)

logger = setup_logger('core.views')


class QuestionListView(generics.ListCreateAPIView):
    def get_queryset(self):
        return Question.objects.prefetch_related('answers').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateQuestionSerializer
        return QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not serializer.validated_data.get('text', '').strip():
            return Response(
                {"error": "Текст вопроса не может быть пустым."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question = serializer.save()
        logger.info(f"Создан новый вопрос с ID {question.id}")
        
        response_serializer = QuestionSerializer(question)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class QuestionDetailView(generics.RetrieveDestroyAPIView):
    queryset = Question.objects.prefetch_related('answers')
    serializer_class = QuestionSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Запрошен вопрос с ID {instance.id}")
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        question_id = instance.id
        self.perform_destroy(instance)
        logger.info(f"Удален вопрос с ID {question_id} и все связанные ответы")
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerCreateView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = CreateAnswerSerializer

    def create(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not serializer.validated_data.get('text', '').strip():
            return Response(
                {"error": "Текст ответа не может быть пустым."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        answer = Answer.objects.create(
            question=question,
            user_id=serializer.validated_data['user_id'],
            text=serializer.validated_data['text']
        )
        
        logger.info(f"Создан ответ с ID {answer.id} для вопроса {question_id}")
        
        response_serializer = AnswerSerializer(answer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class AnswerDetailView(generics.RetrieveDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Запрошен ответ с ID {instance.id}")
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        answer_id = instance.id
        self.perform_destroy(instance)
        logger.info(f"Удален ответ с ID {answer_id}")
        return Response(status=status.HTTP_204_NO_CONTENT)