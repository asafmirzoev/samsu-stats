from django.urls import path

from .views import (
    UserView, UserLogoutView, HomeView, FacultiesView, DepartmentsView, TeachersView,
    CoursesView, DirectionsView, GroupsView, SemestrsView, StatsView, DataView
)


urlpatterns = [
    path('users/', UserView.as_view(), name='user_login'),
    path('users/logout/', UserLogoutView.as_view(), name='user_logout'),

    # path('', HomeView.as_view(), name='home'),

    path('', FacultiesView.as_view(), name='faculties'),
    path('<int:faculty_id>/', FacultiesView.as_view(), name='faculties'),

    path('departments/<int:department_id>/', DepartmentsView.as_view(), name='departments'),
    path('teachers/<int:teacher_id>/', TeachersView.as_view(), name='teachers'),

    path('courses/<int:course_id>/', CoursesView.as_view(), name='courses'),
    path('directions/<int:direction_id>/', DirectionsView.as_view(), name='directions'),
    path('groups/<int:group_id>/', GroupsView.as_view(), name='groups'),
    path('semestrs/<int:semestr_id>/', SemestrsView.as_view(), name='semestrs'),

    path('stats/', StatsView.as_view(), name='stats'),

    path('data/<str:_for>/', DataView.as_view(), name='data'),
]