from django import template

register = template.Library()

@register.filter
# 일련번호 공식 : 일련번호 = 전체 게시물 개수 - 시작 인덱스 - 현재 인덱스 + 1
def sub(value, arg):
    return value - arg