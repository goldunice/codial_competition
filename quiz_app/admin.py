# quiz_app/admin.py

from django.contrib import admin
from .models import CustomUser, QuizField, Question, Option, QuizResult, QuizAnswer


class OptionInline(admin.TabularInline):
    model = Option


class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [OptionInline]


class QuizFieldAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'score')
    search_fields = ('user__username',)
    list_filter = ('user__username',)


class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('quiz_result', 'question', 'selected_option')
    search_fields = ('quiz_result__user__username', 'question__text')
    list_filter = ('quiz_result__user__username', 'question__text')


admin.site.register(CustomUser)
admin.site.register(QuizField, QuizFieldAdmin)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(QuizResult, QuizResultAdmin)
admin.site.register(QuizAnswer, QuizAnswerAdmin)
