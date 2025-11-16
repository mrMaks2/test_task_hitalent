import pytest
import json
from django.urls import reverse
from core.models import Question, Answer
import uuid
from tests.factories import QuestionFactory, AnswerFactory


@pytest.mark.django_db
class TestQuestionAPI:
    def test_get_questions_list(self, client):
        QuestionFactory.create_batch(3)
        
        url = reverse('question-list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert len(response.data['results']) == 3

    def test_create_question(self, client):
        url = reverse('question-list')
        data = {'text': 'New test question?'}
        
        response = client.post(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert Question.objects.count() == 1
        assert Question.objects.first().text == 'New test question?'

    def test_create_empty_question(self, client):
        url = reverse('question-list')
        data = {'text': '   '}
        
        response = client.post(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400

    def test_get_question_detail(self, client):
        question = QuestionFactory.create(text="Test question?")
        
        url = reverse('question-detail', kwargs={'pk': question.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.data['text'] == "Test question?"

    def test_delete_question(self, client):
        question = QuestionFactory.create()
        
        url = reverse('question-detail', kwargs={'pk': question.id})
        response = client.delete(url)
        
        assert response.status_code == 204
        assert Question.objects.count() == 0


@pytest.mark.django_db
class TestAnswerAPI:
    def test_create_answer(self, client):
        question = QuestionFactory.create()
        user_id = str(uuid.uuid4())
        
        url = reverse('answer-create', kwargs={'question_id': question.id})
        data = {
            'user_id': user_id,
            'text': 'Test answer text'
        }
        
        response = client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert Answer.objects.count() == 1
        assert Answer.objects.first().text == 'Test answer text'

    def test_create_answer_invalid_question(self, client):
        user_id = str(uuid.uuid4())
        
        url = reverse('answer-create', kwargs={'question_id': 999})
        data = {
            'user_id': user_id,
            'text': 'Test answer text'
        }
        
        response = client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 404

    def test_get_answer_detail(self, client):
        answer = AnswerFactory.create()
        
        url = reverse('answer-detail', kwargs={'pk': answer.id})
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.data['text'] == answer.text

    def test_delete_answer(self, client):
        answer = AnswerFactory.create()
        
        url = reverse('answer-detail', kwargs={'pk': answer.id})
        response = client.delete(url)
        
        assert response.status_code == 204
        assert Answer.objects.count() == 0