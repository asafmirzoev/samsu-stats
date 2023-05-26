import json

from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User as DefaultUser
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.db import transaction

from .models import (
    Faculty, Department, Teacher, Direction, Course, Group, Semestr, Student, Subject,
    SubjectType, Statistic, TeacherSubjectType, StatisticItem
)
from .choices import SubjectTypes
from .utils import parse_statement_file


def user_login_page(request: HttpRequest):
    return render(request, 'stats/login.html')


def user_login(request: HttpRequest):
    data = request.POST
    username, password = data.get('username'), data.get('password')

    if not (users := DefaultUser.objects.filter(username=username)).exists():
        messages.error(request, 'Пользователь не найден')
        return redirect('user_login')

    user = users.first()
    if not user.check_password(password):
        messages.error(request, 'Неверный пароль')
        return redirect('user_login')
    
    login(request, user)
    messages.success(request, 'Успешный вход')
    return redirect('faculties')


def user_logout(request: HttpRequest):
    logout(request)
    return redirect('user_login')


def home(request: HttpRequest):
    return render(request, 'stats/base.html')


def get_faculties_page(request: HttpRequest):
    faculties = Faculty.objects.all()
    return render(request, 'stats/base/faculties.html', {'faculties': faculties})


def get_faculty_page(request: HttpRequest, faculty_id: int):
    faculty = Faculty.objects.get(pk=faculty_id)
    departments = Department.objects.filter(faculty=faculty)
    courses = Course.objects.filter(faculty=faculty)

    context = {
        'faculty': faculty,
        'departments': departments,
        'courses': courses
    }
    return render(request, 'stats/base/faculty.html', context=context)


def get_department_page(request: HttpRequest, department_id: int):
    department = Department.objects.get(pk=department_id)

    context = {
        'department': department
    }
    return render(request, 'stats/base/department.html', context=context)


def get_course_page(request: HttpRequest, course_id: int):
    course = Course.objects.get(pk=course_id)

    context = {
        'course': course
    }
    return render(request, 'stats/base/course.html', context=context)


def get_direction_page(request: HttpRequest, direction_id: int):
    direction = Direction.objects.get(pk=direction_id)

    context = {
        'direction': direction
    }
    return render(request, 'stats/base/direction.html', context=context)


def get_teacher_page(request: HttpRequest, teacher_id: int):
    teacher = Teacher.objects.get(pk=teacher_id)

    context = {
        'teacher': teacher,
    }
    return render(request, 'stats/base/teacher.html', context=context)


def get_group_page(request: HttpRequest, group_id: int):
    group = Group.objects.get(pk=group_id)

    context = {
        'group': group,
    }
    return render(request, 'stats/base/group.html', context=context)

def get_semestr_page(request: HttpRequest, semestr_id: int):
    semestr = Semestr.objects.get(pk=semestr_id)

    stats = {
        str(_('Показатель успеваемости')): [],
        str(_('Показатель качества')): [],
        5: [],
        4: [],
        3: [],
        2: [],
    }

    for grade in stats.keys():
        for subject in semestr.subject_set.all():

            if not hasattr(subject, 'statistic'):
                stats[grade].append('')
                continue

            if isinstance(grade, int): count = sum([1 for stat_item in subject.statistic.statisticitem_set.all() if stat_item.grade == grade])
            
            if grade == str(_('Показатель успеваемости')):
                count = f'{subject.performance}%'
            
            if grade == str(_('Показатель качества')):
                count = f'{subject.quality}%'

            stats[grade].append(count)

    context = {
        'semestr': semestr,
        'stats': stats,
    }
    return render(request, 'stats/base/semestr.html', context=context)


def get_stats_page(request: HttpRequest):
    faculties = Faculty.objects.all()
    subject_types = SubjectTypes.choices

    context = {
        'faculties': faculties,
        'subject_types': subject_types
    }

    return render(request, 'stats/base/stats.html', context=context)


def upload_statement(request: HttpRequest):
    data, files = request.POST, request.FILES
    faculty_id, course_id, subject_id, group_id, file, teachers = data.get('faculty'), data.get('course'), data.get('subject'), data.get('group'), files.get('file'), data.get('_teachers')

    with transaction.atomic():
        course = Course.objects.get(pk=course_id, faculty_id=faculty_id)
        group = Group.objects.get(pk=group_id, direction__course=course)
        subject = Subject.objects.get(pk=subject_id)

        data = parse_statement_file(file)
        if not data: return redirect('stats')

        teachers_subject_types = []
        for teacher in json.loads(teachers):
            subject_type, _ = SubjectType.objects.get_or_create(name=teacher.get('subject_type'), subject=subject, teacher_id=int(teacher.get('teacher_id')))
            teacher_sub_type, _ = TeacherSubjectType.objects.get_or_create(teacher_id=int(teacher.get('teacher_id')), subject_type=subject_type)
            teachers_subject_types.append(teacher_sub_type)
        
        statistic, _ = Statistic.objects.get_or_create(group=group, subject=subject)
        statistic.teachers_subject_types.add(*teachers_subject_types)

        stats, stats_update = [], []
        for stat in data:
            student, _ = Student.objects.get_or_create(name=stat['name'], group=group)

            if (stat_item := StatisticItem.objects.filter(stat=statistic, student=student)).exists():
                stat_item = stat_item.first()
                stat_item.semestr_total, stat_item.final_control, stat_item.grade = stat['semestr_total'], stat['final_control'], stat['grade']
                stats_update.append(stat_item)
                continue

            stats.append(StatisticItem(
                stat=statistic,
                student=student,
                semestr_total=stat['semestr_total'],
                final_control=stat['final_control'],
                grade=stat['grade']
            ))
            
        StatisticItem.objects.bulk_create(stats)
        StatisticItem.objects.bulk_update(stats_update, ['semestr_total', 'final_control', 'grade'])

    return redirect('semestrs', semestr_id=subject.semestr.pk)


def get_courses_data(request: HttpRequest):
    faculty_id = request.GET.get('faculty_id')
    if not faculty_id: return JsonResponse({})

    courses = {course.pk: course.course for course in Course.objects.filter(faculty_id=faculty_id)}
    return JsonResponse(courses)


def get_directions_data(request: HttpRequest):
    course_id = request.GET.get('course_id')
    if not course_id: return JsonResponse({})

    directions = {direction.pk: direction.name for direction in Direction.objects.filter(course_id=course_id)}
    return JsonResponse(directions)


def get_groups_data(request: HttpRequest):
    direction_id = request.GET.get('direction_id')
    if not direction_id: return JsonResponse({})

    groups = {group.pk: group.name for group in Group.objects.filter(direction_id=direction_id)}
    return JsonResponse(groups)


def get_semestrs_data(request: HttpRequest):
    group_id = request.GET.get('group_id')
    if not group_id: return JsonResponse({})

    semestrs = {semestr.pk: semestr.semestr for semestr in Semestr.objects.filter(group_id=group_id)}
    return JsonResponse(semestrs)


def get_subjects_data(request: HttpRequest):
    semestr_id = request.GET.get('semestr_id')
    if not semestr_id: return JsonResponse({})

    subjects = {subject.pk: subject.name for subject in Subject.objects.filter(semestr_id=semestr_id)}
    return JsonResponse(subjects)


def get_departments_data(request: HttpRequest):
    faculty_id = request.GET.get('faculty_id')
    if not faculty_id: return JsonResponse({})

    departments = {department.pk: department.name for department in Department.objects.filter(faculty_id=faculty_id)}
    return JsonResponse(departments)


def get_teachers_data(request: HttpRequest):
    department_id = request.GET.get('department_id')
    if not department_id: return JsonResponse({})

    teachers = {teacher.pk: teacher.name for teacher in Teacher.objects.filter(department_id=department_id).order_by('name')}
    return JsonResponse(teachers)
