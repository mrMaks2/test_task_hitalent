# tests/factories.py
import factory
from core.models import Question, Answer
import uuid


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    text = factory.Faker('sentence')


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    user_id = factory.LazyFunction(uuid.uuid4)
    text = factory.Faker('sentence')