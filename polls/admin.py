from django.contrib import admin
from polls.models import *

class ChocieInline(admin.TabularInline): #tabularinline=테이블 형식
    model=Choice
    extra=3 #admin 화면에 보이는 것만 3개. chocie 추가 가능

class QuestionAdmin(admin.ModelAdmin): #필드 순서를 조정가능, 제목부터나옴
    fieldsets = [
        ('Question Statement', {'fields':['question_text']}),
        ('Date information', {'fields':['pub_date'],'classes':['collapse']}),
    ]

    inlines=[ChocieInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently') #레코드 컬럼

    list_filter = ['pub_date'] #pub date를 기준으로 필터링
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
# Register your models here.
