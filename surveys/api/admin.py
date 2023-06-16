from django import forms
from django.contrib import admin
from django.forms.widgets import SelectDateWidget

from .models import Survey, Question, Answer, Variant


class SurveyForm(forms.ModelForm):
    # end_date = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     label='Дата окончания',
    # )

    class Meta:
        model = Survey
        fields = ('__all__')
        widgets = {
            "end_date": SelectDateWidget(),
        }


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    form = SurveyForm
    fields = (
        'name', 'description', 'start_date', 'end_date', 'is_active', 'user',
    )
    readonly_fields = ('start_date',)
    list_display = (
        'id', 'name', 'description', 'start_date', 'end_date', 'is_active',
        'user',
    )
    list_editable = ('is_active',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = (
        'type', 'text', 'survey',
    )
    list_display = (
        'id', 'type', 'text', 'survey',
    )


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    fields = (
        'text', 'question',
    )
    list_display = (
        'id', 'text', 'question',
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fields = (
        'answer', 'survey', 'question',
    )
    list_display = (
        'user_id', 'answer', 'survey', 'question',
    )
