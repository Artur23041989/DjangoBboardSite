from django import forms
from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')

 # Форма для занесения сведений о новом пользователе
class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=False, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                                help_text='Введите тот же самы пароль еще раз для проверки')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают',
                                                   code = 'password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True # пользователь активен (True)
        user.is_activated = True # пользователь прошел активацию (True)
        if commit:
            user.save()
         #   post_register.send(RegisterForm, isinstance=user) # отправка сигнала с требованием активации
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'send_messages')

class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(),
                                          empty_label=None,
                                          label='Надрубрика',
                                          required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'

class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')

class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}
AIFormSet = forms.inlineformset_factory(Bb, AdditionalImage, fields = '__all__')





