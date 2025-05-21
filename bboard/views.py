from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin # вывод всплывающих сообщений об успешном вполнении операции
from django.contrib.auth.mixins import LoginRequiredMixin # суперкласс, запрещающий доступ к контроллеру гостям
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import AdvUser
from .forms import ProfileEditForm, RegisterForm
from django.views.generic.base import TemplateView
from django.contrib.auth import logout




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

class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'bboard/profile_edit.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('bboard:profile')
    success_message = 'Данные пользователя изменены'

    # получение ключа текущего пользователя
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request,*args, **kwargs)

    # извлечение исправляемой записи текущего пользователя
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class PasswordEditView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'bboard/password_edit.html'
    success_url = reverse_lazy('bboard:profile')
    success_message = 'Пароль пользователя изменен'

# регистрация пользователя
class RegisterView(CreateView):
    model = AdvUser
    template_name = 'bboard/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('bboard:register_done')

# вывод сообщения об успешной регистрации

class RegisterDoneView(TemplateView):
    template_name = 'bboard/register_done.html'

# удаление пользователя
class ProfileDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'bboard/profile_delete.html'
    success_url = reverse_lazy('bboard:index')
    success_message = 'Пользователь удален'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
