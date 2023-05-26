from django.views import View
from django.http import HttpRequest, Http404, HttpResponse

from . import services as svc


class UserView(View):

    def get(self, request: HttpRequest):
        return svc.user_login_page(request)

    def post(self, request: HttpRequest):
        return svc.user_login(request)


class UserLogoutView(View):

    def get(self, request: HttpRequest):
        return svc.user_logout(request)


class HomeView(View):

    def get(self, request: HttpRequest):
        return svc.home(request)


class FacultiesView(View):

    def get(self, request: HttpRequest, faculty_id: int = None):
        if faculty_id: return svc.get_faculty_page(request, faculty_id)
        return svc.get_faculties_page(request)


class DepartmentsView(View):

    def get(self, request: HttpRequest, department_id: int):
        return svc.get_department_page(request, department_id)


class TeachersView(View):

    def get(self, request: HttpRequest, teacher_id: int):
        return svc.get_teacher_page(request, teacher_id)


class CoursesView(View):

    def get(self, request: HttpRequest, course_id: int):
        return svc.get_course_page(request, course_id)


class DirectionsView(View):

    def get(self, request: HttpRequest, direction_id: int):
        return svc.get_direction_page(request, direction_id)


class GroupsView(View):

    def get(self, request: HttpRequest, group_id: int):
        return svc.get_group_page(request, group_id)


class SemestrsView(View):

    def get(self, request: HttpRequest, semestr_id: int):
        return svc.get_semestr_page(request, semestr_id)
    

class StatsView(View):

    def get(self, request: HttpRequest):
        return svc.get_stats_page(request)
    
    def post(self, request: HttpRequest):
        return svc.upload_statement(request)


class DataView(View):

    def get(self, request: HttpRequest, _for: str = None):
        if _for == 'courses-by-faculty': return svc.get_courses_data(request)
        if _for == 'directions-by-course': return svc.get_directions_data(request)
        if _for == 'groups-by-direction': return svc.get_groups_data(request)
        if _for == 'semestrs-by-group': return svc.get_semestrs_data(request)
        if _for == 'subjects-by-semestr': return svc.get_subjects_data(request)
        if _for == 'departments-by-faculty': return svc.get_departments_data(request)
        if _for == 'teachers-by-department': return svc.get_teachers_data(request)
        raise Http404()