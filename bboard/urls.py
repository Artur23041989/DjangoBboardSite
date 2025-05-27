from django.urls import path
from .views import (index, other_page, BBLoginView, profile, BBLogoutView,
                    ProfileEditView, PasswordEditView, RegisterView,
                    RegisterDoneView, ProfileDeleteView, rubric_bbs, bb_detail)


app_name = 'bboard'
urlpatterns = [
    path('accounts/register/done', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register', RegisterView.as_view(), name='register'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('account/password/edit', PasswordEditView.as_view(), name='password_edit'),
    path('accounts/profile/delete', ProfileDeleteView.as_view(), name='profile_delete'),
    path('accounts/profile/edit', ProfileEditView.as_view(), name='profile_edit'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('<int:rubric_pk>/<int:pk>/', bb_detail, name='bb_detail'),
    path('<int:pk>/', rubric_bbs, name='rubric_bbs'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index')
]

