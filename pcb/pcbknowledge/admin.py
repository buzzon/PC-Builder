from django.contrib import admin
import nested_admin
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

