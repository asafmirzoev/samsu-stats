import json

from django.db import transaction

from .models import Faculty, Department, Teacher, Direction, Course, Group, Semestr, Subject


class InitData:

    def __init__(self):

        self.facs_file: dict = json.load(open('data/faculties.json', 'r', encoding='utf-8'))
        self.deps_file: dict = json.load(open('data/data.json', 'r', encoding='utf-8'))
        self.groups_file: dict = json.load(open('data/groups.json', 'r', encoding='utf-8'))
        self.subjects_file: dict = json.load(open('data/subjects.json', 'r', encoding='utf-8'))
    
    def run(self):
        with transaction.atomic():
            self.init_faculties()
            self.init_departments_and_teachers()
            self.init_directs_and_groups()
            self.init_subjects()
    
    def init_faculties(self):
        facs = [
            Faculty(name_ru=faculty.get('name_ru'), name_uz=faculty.get('name_uz')) for faculty_id, faculty in self.facs_file.items() if not Faculty.objects.filter(name_ru=faculty.get('name_ru')).exists()
        ]
        if facs: Faculty.objects.bulk_create(facs)
    
    def init_departments_and_teachers(self):
        deps = []
        teachers = []
        teachers_names = []

        for faculty_id, _departments in self.deps_file.items():
            for department, _teachers in _departments.items():
                if not Department.objects.filter(faculty_id=faculty_id, name__icontains=department).exists():
                    department = Department(faculty_id=faculty_id, name=department)
                    deps.append(department)
                else:
                    department = Department.objects.get(faculty_id=faculty_id, name__icontains=department)
                for teacher_name in _teachers:
                    if not Teacher.objects.filter(name__icontains=teacher_name).exists() and teacher_name not in teachers_names:
                        teachers.append(Teacher(name=teacher_name, department=department))
                        teachers_names.append(teacher_name)
                            
        if deps: Department.objects.bulk_create(deps)
        if teachers: Teacher.objects.bulk_create(teachers)
    
    def init_directs_and_groups(self):
        directs = []
        courses = []
        groups = []

        for faculty_name, directions in self.groups_file.items():
            faculty = Faculty.objects.get(name_uz=faculty_name)
            for course, _directions in directions.items():
                if (_course := Course.objects.filter(course=int(course), faculty=faculty)).exists():
                    course_ = _course.first()
                else:
                    course_ = Course(course=int(course), faculty=faculty)
                    courses.append(course_)
                
                for direction_name, _groups in _directions.items():

                    if (direction := Direction.objects.filter(name=direction_name, course=course_)).exists():
                        direction = direction.first()
                        direction.course = course_
                        direction.save()
                    else:
                        direction = Direction(name=direction_name, course=course_)
                        directs.append(direction)

                    for group_name, group_data in _groups.items():
                        if not (group := Group.objects.filter(name=group_name, direction=direction, education_form=group_data['education_form'], language=group_data['language'])).exists():
                            group = Group(name=group_name, direction=direction, education_form=group_data['education_form'], language=group_data['language'])
                            groups.append(group)

        Course.objects.bulk_create(courses)
        Direction.objects.bulk_create(directs)
        Group.objects.bulk_create(groups)
    
    def init_subjects(self):
        semestrs = []
        subjects = []

        for direction_name, _semestrs in self.subjects_file.items():
            direction = Direction.objects.get(name=direction_name)
            for semestr, _subjects in _semestrs.items():
                for group in Group.objects.filter(direction=direction):
                    if (_semestr := Semestr.objects.filter(group=group, semestr=int(semestr))).exists():
                        semestr_ = _semestr.first()
                    else:
                        semestr_ = Semestr(group=group, semestr=int(semestr))
                        semestrs.append(semestr_)

                    for subjects_data in _subjects:
                        if not Subject.objects.filter(semestr=semestr_, name=subjects_data['subject_name']).exists(): subjects.append(Subject(semestr=semestr_, name=subjects_data['subject_name'], hours=subjects_data['hours'], credits=subjects_data['credits'], type=subjects_data['subject_type']))
        
        Semestr.objects.bulk_create(semestrs)
        Subject.objects.bulk_create(subjects)


def parse_statement_file(file):
    import pandas as pd
    
    data = []

    xl_file = pd.read_excel(file, header=None)
    df = xl_file.where(pd.notnull(xl_file), None)

    for i, (index, name, student_id, n1, n2, semestr_total, final_control, total, grade) in df.iterrows():
        data.append({
            'name': name.strip(),
            'semestr_total': round(semestr_total, 2),
            'final_control': round(final_control, 2),
            'grade': int(grade)
        })
    return data


def get_grade_color(grade: int):
    colors = {
        1: '#000000',
        2: '#FF0000',
        3: '#FFFF00',
        4: '#00FFA8',
        5: '#75FF71'
    }
    return colors[grade]