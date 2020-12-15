from django.contrib import admin
import nested_admin
from django.contrib.admin import AdminSite

from .models import *

admin.site.register(ComponentVariable)
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

    def save_model(self, request, obj, form, change):
        if obj.is_first and Question.objects.count() > 1:
            Question.objects.update(is_first=False)
        super(QuestionAdmin, self).save_model(request, obj, form, change)


admin.site.register(Question, QuestionAdmin)


class ExpertAdminSite(AdminSite):
    site_header = 'Expert Page'
    site_title = 'Expert Page'
    index_title = 'Created by .DCP'


expert = ExpertAdminSite(name='expert')
expert.register(Question, QuestionAdmin)
expert.register(ComponentVariable)
