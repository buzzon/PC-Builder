from django.contrib import admin
import nested_admin
from django.contrib.admin import AdminSite

from .models import *

admin.site.register(Component)
admin.site.register(Build)


class FactorInline(nested_admin.NestedTabularInline):
    model = Factor
    extra = 0


class EssenceInline(nested_admin.NestedStackedInline):
    model = Essence
    extra = 0
    inlines = [FactorInline]
    fk_name = 'question'


class QuestionAdmin(nested_admin.NestedModelAdmin):
    inlines = [EssenceInline]


admin.site.register(Question, QuestionAdmin)


class ExpertAdminSite(AdminSite):
    site_header = 'Expert Page'
    site_title = 'Expert Page'
    index_title = 'Created by .DCP'


expert = ExpertAdminSite(name='expert')
expert.register(Question, QuestionAdmin)
