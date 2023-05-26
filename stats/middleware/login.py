from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import redirect


class SetUserLoginMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if not request.user.is_authenticated and request.path != reverse('user_login'):
            return redirect('user_login')
        
        if request.user.is_authenticated and request.path == reverse('user_login'):
            return redirect('faculties')
        
    def process_response(self, request, response):
        return response