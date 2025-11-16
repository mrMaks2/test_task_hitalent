from django.db import models
from django.utils import timezone
import uuid


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(verbose_name="Текст вопроса")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Вопрос с ID {self.id}: {self.text[:50]}..."


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Вопрос"
    )
    user_id = models.UUIDField(default=uuid.uuid4, verbose_name="ID пользователя")
    text = models.TextField(verbose_name="Текст ответа")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ['created_at']

    def __str__(self):
        return f"Ответ с ID {self.id} к Вопросу с ID {self.question_id}"