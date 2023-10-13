from django.db import models

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)  # 질문의 제목. 글자 수를 제한가고 싶을때는 CharField를 사용
    content = models.TextField()  # 질문의 내용
    create_date = models.DateTimeField()  # 질문 작성일

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 질문(어떤 질문의 답변인지를 표시). on_delete=models.CASCADE = 질문이 삭제되면 답변도 삭제
    content = models.TextField()  # 답변의 내용
    create_date = models.DateTimeField()  # 답변 작성일