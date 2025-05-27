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
from .models import AdvUser, SubRubric, Bb
from .forms import ProfileEditForm, RegisterForm, SearchForm
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Q




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

def rubric_bbs(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword':keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {
        'rubric': rubric,
        'page': page,
        'bbs': page.object_list,
        'form': form
    }
    return render(request, 'bboard/rubric_bbs.html', context)

def bb_detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'bboard/bb_detail.html', context)


