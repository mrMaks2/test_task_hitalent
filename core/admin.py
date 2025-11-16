from django.contrib import admin
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_short', 'created_at', 'answers_count']
    list_filter = ['created_at']
    search_fields = ['text']
    inlines = [AnswerInline]

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст'

    def answers_count(self, obj):
        return obj.answers.count()
    answers_count.short_description = 'Количество ответов'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'user_id', 'text_short', 'created_at']
    list_filter = ['created_at', 'question']
    search_fields = ['text', 'user_id']

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст'