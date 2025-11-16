import pytest
from django.utils import timezone
from core.models import Question, Answer
import uuid


@pytest.mark.django_db
class TestQuestionModel:
    def test_create_question(self):
        question = Question.objects.create(text="Test question?")
        assert question.text == "Test question?"
        assert question.id is not None
        assert question.created_at <= timezone.now()

    def test_question_str(self):
        question = Question.objects.create(text="Test question?")
        # Исправлено: проверяем русское представление
        assert str(question).startswith("Вопрос с ID")
        assert "Test question?" in str(question)


@pytest.mark.django_db
class TestAnswerModel:
    def test_create_answer(self):
        question = Question.objects.create(text="Test question?")
        user_id = uuid.uuid4()
        answer = Answer.objects.create(
            question=question,
            user_id=user_id,
            text="Test answer"
        )
        
        assert answer.question == question
        assert answer.user_id == user_id
        assert answer.text == "Test answer"
        assert answer.id is not None

    def test_cascade_delete(self):
        question = Question.objects.create(text="Test question?")
        Answer.objects.create(
            question=question,
            user_id=uuid.uuid4(),
            text="Test answer"
        )
        
        assert Answer.objects.count() == 1
        question.delete()
        assert Answer.objects.count() == 0