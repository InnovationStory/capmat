from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('students:first_page')
        else:
            return redirect('students:first_page')
            
    return render(request, 'classroom/home.html')
