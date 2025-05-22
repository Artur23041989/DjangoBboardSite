from django.contrib import admin
from .models import AdvUser, SuperRubric, SubRubric
from .forms import SubRubricForm


admin.site.register(AdvUser)
# Register your models here.

class SubRubricInline(admin.TabularInline):
    model = SubRubric

class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)
admin.site.register(SuperRubric, SuperRubricAdmin)

class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm
admin.site.register(SubRubric, SubRubricAdmin)
