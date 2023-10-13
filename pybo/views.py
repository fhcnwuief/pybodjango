from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

# Create your views here.
def index(request):
    """
    pybo 목록 출력
    render 함수는 context에 있는 모델 데이터를 pybo/quesion_list.html(템플렛이라고 부른다)파일에 적용하여 HTML코드로 변환
    """
    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지

    # 조회
    question_list = Question.objects.order_by('-create_date')  # 작성일시 역순으로

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)
    # return HttpResponse("안녕하세요! pybo에 오신것을 환영합니다.")

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)  # Question.objects.get(id=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id = question_id)
    else:
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request ,'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm() # request.method가 'GET'인 경우 호출
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """pybo 질문 수정"""
    question = get_object_or_404(Question, pk = question_id)
    if request.user != question.author:
        messages.error(reqeust, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)  # instance를 이용하여 기존 값을 폼에 채워넣는다.
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  #수정일 저장
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """질문 삭제"""
    question = get_object_or_404(Question, pk = question_id)
    if request.user != question.author:
        messages.error(request, "삭제권한이 없습니다.")
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """pybo 답변 수정"""
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(reqeust, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)  # instance를 이용하여 기존 값을 폼에 채워넣는다.
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()  #수정일 저장
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer':answer, 'form':form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """답변 삭제"""
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(request, "삭제권한이 없습니다.")
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)