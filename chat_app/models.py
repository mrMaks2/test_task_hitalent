from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

class Chat(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(1, message="Заголовок не может быть пустым."),
            MaxLengthValidator(200, message="Заголовок не может превышать 200 символов.")
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Удаление лишних пробелов из заголовка
        if self.title:
            self.title = self.title.strip()
        super().save(*args, **kwargs)


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    text = models.TextField(
        validators=[
            MinLengthValidator(1, message="Текст не может быть пустым."),
            MaxLengthValidator(5000, message="Текст не может превышать 5000 символов.")
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Сообщение в  {self.chat.title}: {self.text[:50]}..."

    def save(self, *args, **kwargs):
        # Удаление лишних пробелов из текста
        if self.text:
            self.text = self.text.strip()
        super().save(*args, **kwargs)