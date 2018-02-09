from django.db import models
from django.utils import timezone


class Magazine(models.Model):
    title = models.CharField('Название журнала')

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'


class Number(models.Model):
    magazine = models.ForeignKey(Magazine, on_delete=models.SET_NULL)
    number = models.PositiveSmallIntegerField('Номер')
    through_number = models.PositiveSmallIntegerField('Сквозной номер')
    release_date = models.DateField('Дата выпуска', default=timezone.now)

    class Meta:
        verbose_name = 'Номер журнала'
        verbose_name_plural = 'Номера журнала'
