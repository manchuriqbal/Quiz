from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import random
from .models import *

def home(request):
    context = {'categories': Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"quiz/?category={request.GET.get('category')}")
    return render(request, 'home.html', context)

def quiz(request):
    context = {'category' : request.GET.get('category')}
    return render(request, 'quiz.html', context)

def get_quiz(request):
    try:
        question_obj =Question.objects.all()
        if request.GET.get('category'):
            question_obj = question_obj.filter(category__category_name__icontains=request.GET.get('category'))
        question_obj =list(question_obj)
        data = []
        random.shuffle(question_obj)
        for question in question_obj:
            data.append({
                'uuid' : question.uuid,
                'category': question.category.category_name,
                'question' : question.question_text,
                'marks': question.marks,
                'answer': question.get_answer()
            })
        payload = {'status': True, 'data': data}

        return JsonResponse(payload)

    except Exception as e:
        print(e)