from django.db import models

from .choices import EducationForms, EducationLanguages, SubjectTypeChoice, SubjectTypes


class Faculty(models.Model):

    name = models.CharField('Название', max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'


class Department(models.Model):

    name = models.CharField('Название', max_length=255, unique=True)
    faculty = models.ForeignKey(Faculty, verbose_name='Факультет', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'


class Teacher(models.Model):

    name = models.CharField('Имя', max_length=255, unique=True)
    department = models.ForeignKey(Department, verbose_name='Кафедра', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Course(models.Model):

    course = models.PositiveSmallIntegerField('Курс')
    faculty = models.ForeignKey(Faculty, verbose_name='Факультет', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Direction(models.Model):

    name = models.CharField('Имя', max_length=255, unique=True)
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'


class Group(models.Model):

    name = models.CharField('Имя', max_length=255, unique=True)
    direction = models.ForeignKey(Direction, verbose_name='Направление', on_delete=models.CASCADE)
    education_form = models.CharField('Форма обучения', max_length=32, choices=EducationForms.choices)
    language = models.CharField('Язык обучения', max_length=32, choices=EducationLanguages.choices)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Semestr(models.Model):

    group = models.ForeignKey(Group, verbose_name='Группа', on_delete=models.CASCADE)
    semestr = models.PositiveSmallIntegerField('Семестр')

    def __str__(self):
        return str(self.semestr)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'



class Subject(models.Model):
    
    semestr = models.ForeignKey(Semestr, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    hours = models.PositiveSmallIntegerField('Часы')
    credits = models.PositiveSmallIntegerField('Кредиты')
    type = models.CharField('Тип предмета', max_length=64, choices=SubjectTypeChoice.choices)

    def __str__(self):
        return f'{self.name}'
    
    @property
    def performance(self):
        return round(sum([stat_item.grade for stat_item in self.statistic.statisticitem_set.all() if stat_item.grade != 2]) / (self.statistic.statisticitem_set.count() * 5) * 100)
    
    @property
    def performance_count(self):
        return self.statistic.statisticitem_set.filter(grade__gt=2).count()
    
    @property
    def bad_performance(self):
        return round(100 - self.performance)
    
    @property
    def bad_performance_count(self):
        return self.statistic.statisticitem_set.all().count() - self.performance_count
    
    @property
    def quality(self):
        return round(sum([stat_item.grade for stat_item in self.statistic.statisticitem_set.all() if stat_item.grade in [4, 5]]) / (self.statistic.statisticitem_set.count() * 5) * 100)

    @property
    def quality_count(self):
        return self.statistic.statisticitem_set.filter(grade__in=[4, 5]).count()
    
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class SubjectType(models.Model):

    name = models.CharField(max_length=255, choices=SubjectTypes.choices)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип занятия'
        verbose_name_plural = 'Типы занятий'
    

class Student(models.Model):

    name = models.CharField('Имя', max_length=255)
    group = models.ForeignKey(Group, verbose_name='Группа', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Statistic(models.Model):

    group = models.ForeignKey(Group, verbose_name='Группа', on_delete=models.CASCADE)
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE)
    teachers_subject_types = models.ManyToManyField('TeacherSubjectType', verbose_name='Препод')

    def __str__(self):
        return f'Statistic: {self.pk}'
    
    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'


class TeacherSubjectType(models.Model):

    teacher = models.ForeignKey(Teacher, verbose_name='Препод', on_delete=models.CASCADE)
    subject_type = models.ForeignKey(SubjectType, on_delete=models.CASCADE)



class StatisticItem(models.Model):

    stat = models.ForeignKey(Statistic, verbose_name='Statistic', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.CASCADE)

    semestr_total = models.FloatField('Баллы в семестре', max_length=5)
    final_control = models.FloatField('Итоговый контроль', max_length=5)
    grade = models.PositiveSmallIntegerField('Итоговый контроль')
    
    def __str__(self):
        return f'StatisticItem: {self.pk}'
    
    @property
    def total(self):
        return round(self.semestr_total + self.final_control, 1)
    
    class Meta:
        verbose_name = 'Статистика[ITEM]'
        verbose_name_plural = 'Статистика[ITEM]'


