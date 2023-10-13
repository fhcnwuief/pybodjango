from django.urls import path
from . import views

app_name = 'pybo'  # 서로 다른 앱이 같은 url매핑 별칭을 쓸 때 중복문제 발생. namespace 도입

urlpatterns = [
    path('', views.index, name = 'index'),  # name 속성으로 url 매핑에 별칭만들기
    path('<int:question_id>/', views.detail, name = 'detail'),  # /pybo/2/ 요청시, question_id에 2가 저장 --> views.detail함수 실행
    path('answer/create/<int:question_id>', views.answer_create, name = 'answer_create'),
    path('question/create/', views.question_create, name = 'question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name = 'question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name = 'question_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name = 'answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name = 'answer_delete'),
]