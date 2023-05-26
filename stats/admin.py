from django.contrib import admin

from .models import Faculty, Department, Group, Teacher, Student, Subject, Statistic, StatisticItem


admin.site.site_header = 'Администрирование'
admin.site.site_title = 'Администрирование'


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    pass


@admin.register(StatisticItem)
class StatisticItemAdmin(admin.ModelAdmin):
    pass