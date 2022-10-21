from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
# Create your views here.
from django.template import loader
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice


class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'

    #return the last five published questions
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model=Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model=Question
    template_name = 'polls/results.html'


# def index(request): #투표목록이 보이도록 해야함
#     #-pub_date: 역순으로 나열
#     latest_question_list = Question.objects.order_by('-pub_date')[:5] #5개의 데이터를 보여줘라. 모델에 정의한 question 테이블 의미
#     #template=loader.get_template('polls/index.html')
#     #output = ', '.join([q.question_text for q in latest_question_list]) #문자열에 제공되는 join 메소드. q를 한 번씩 순회하면서 가져오기
#     context={'latest_question_list': latest_question_list}
#     #return HttpResponse(output) #output을 string 형태로 만들어주기
#
#     return render(request, 'polls/index.html', context)
#
# def detail(request, question_id):
#    question=get_object_or_404(Question, pk=question_id)
#    #Http404=get_object_or_404
#    return render(request, 'polls/detail.html', {'question':question})
#
# def results(request, question_id):
#     question=get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice']) #choice와 같은 항목을 select_chocie에 넣어주기
    except(KeyError, Choice.DoesNotExist): #아니면 error에 넣어주기
        return render(request, 'polls/detail.html', {'question':question, 'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes +=1
        selected_choice.save()

        #reverse 함수=>url 패턴 이름 받음
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))