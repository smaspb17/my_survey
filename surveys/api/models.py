# import uuid
from datetime import date
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Survey(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название'
    )
    start_date = models.DateField(
        # default=date.today,
        # default=timezone.localdate,
        verbose_name='Дата старта',
    )
    end_date = models.DateField(
        verbose_name='Дата окончания'
    )
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Админ',
    )

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def clean(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            if delta.days < 3:
                raise ValidationError(
                    {'end_date':
                        'Дата окончания - не менее 3 дней от даты старта.'}
                )

    def __str__(self):
        return f'{self.name} №{self.pk}'

#     def check_survey(self):
#         if self.end_date < timezone.now().date():
#             self.is_active = False
#             self.save()


# # сигнал на деактивацию опроса по истечении срока
# @receiver(post_save, sender=Survey)
# def survey_expire(sender, instance, **kwargs):
#     instance.check_survey()

# # это не работает!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
# @receiver(post_save, sender=Survey)
# def set_survey_expired(sender, instance, **kwargs):
#     if timezone.localdate() > instance.end_date:
#         instance.is_active = False
#         instance.save()


class Question(models.Model):
    class Type(models.TextChoices):
        TEXT = 'Текст'
        CHOOSING_ONE = 'Выбор одного варианта ответа'
        CHOOSING_MULTIPLE = 'Выбор нескольких вариантов ответов'
    type = models.CharField(
        verbose_name='Тип ответа',
        max_length=len(max(Type.values, key=len)),
        choices=Type.choices,
        default=Type.TEXT,
    )
    text = models.TextField(verbose_name='Текст вопроса')
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Опрос',
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text


class Variant(models.Model):
    text = models.TextField(verbose_name='Текст варианта ответа')
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name='Вопрос'
    )

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        return self.text


class Answer(models.Model):
    user_id = models.IntegerField()
    answer = models.TextField(verbose_name='Ответ пользователя')
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Опрос',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос',
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
