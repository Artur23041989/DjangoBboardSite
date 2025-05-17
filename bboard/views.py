from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'bboard/index.html')

def other_page(request, page):
    try:
        template = get_template('bboard/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class BBLoginView(LoginView):
    template_name = 'bboard/login.html'

class BBLogoutView(LogoutView):
    pass

@login_required
def profile(request):
    return render(request, 'bboard/profile.html')

