from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class EducationForms(TextChoices):

    KUNDUZGI = 'Kunduzgi', _('Дневное')
    KECHKI = 'Kechki', _('Вечернее')


class EducationLanguages(TextChoices):

    OZBEK = 'O‘zbek', _('Узбекский')
    RUS = 'Rus', _('Русский')


class SubjectTypeChoice(TextChoices):

    MAJBURIY = 'Majburiy', _('Обязательный')
    TANLOV = 'Tanlov', _('Выборочный')
    BOSHQA = 'Boshqa', _('Другой')


class SubjectTypes(TextChoices):

    MARUZA = "Ma'ruza", _("Лекция")
    AMALIY = 'Amaliy', _("Практика")
    LABORATORIYA = 'Laboratoriya', _("Лаборатория")