from django.db import IntegrityError
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from app import forms
from django.contrib.auth.decorators import login_required
from . import models

from datetime import datetime, timezone, timedelta

from django.contrib import auth


'''
    Задачи
    - Логин создает юзера, а нужно профиль
        - аватарка
    - В settings добавить аватарку
    - textArea вопроса слишком большой
    - декомпозировать контроллеры
    - get_shared_context не нужен
    - проверить частные случаи
    - определить поля, обязательные для заполнения
    - теги без запятой?
    - проверить выполнение всех задач с гитхаба (не все выполнены)
        - contunue например
'''

COUNT_BEST_ITEMS = 10

def paginate(objects_list, request, per_page = 5):
    contact_list = objects_list
    paginator = Paginator(contact_list, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    print(page)
    print(type(page))
    print(page.object_list)
    return page

def get_best_items():
    best_items = {
        'tags' : models.Tag.objects.get_popular_tags()[:COUNT_BEST_ITEMS],
        'profiles' : models.Profile.objects.get_best_profiles()[:COUNT_BEST_ITEMS]
    }
    return best_items

def get_shared_context():
    return {
        'best_items'    : get_best_items()
    }
    

def index(request):
    questions = models.Question.objects.get_new_questions()
    page = paginate(questions, request)
    context = get_shared_context()
    context['page'] = page
    context['is_hot'] = False
    return render(request, "index.html", context=context)

def hot(request):
    hot_questions = models.Question.objects.get_hot_questions()
    page = paginate(hot_questions, request)
    context = get_shared_context()
    context['page'] = page
    context['is_hot'] = True
    return render(request, "hot.html", context=context)

def question(request, question_id : int):
    needed_question = models.Question.objects.filter(pk=question_id)
    if not needed_question.exists():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    needed_question = needed_question[0]
    answers = needed_question.answer_set.all().order_by('-date')
    page = paginate(answers, request)
    if request.method == 'GET':
        answer_form = forms.AnswerForm()
    elif request.method == 'POST':
        answer_form = forms.AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit = False)
            
            user = models.User.objects.get(username = request.user)
            answer.author = models.Profile.objects.get(user = user)

            answer.question = needed_question
            answer.save()
            # обновление страницы, чтобы появился ответ
            return redirect(request.META['HTTP_REFERER'])
            
            
    context = get_shared_context()
    context['question'] = needed_question
    context['page'] = page
    context['form'] = answer_form
    return render(request, "question.html", context=context)

def ask(request):
    if request.method == 'GET':
        ask_form = forms.AskForm()
    elif request.method == 'POST':
        ask_form = forms.AskForm(request.POST)
        if ask_form.is_valid():
            # получаем объект БД
            question = ask_form.save(commit = False)
            user = models.User.objects.get(username = request.user)
            question.author = models.Profile.objects.get(user = user)
            question.save()
            for tag_title in ask_form.cleaned_data['tag_list'].split():
                tag = models.Tag(title = tag_title)
                try:
                    tag.save()
                    question.tags.add(tag)
                except IntegrityError:
                    pass
            return redirect(reverse("index"), question_id=question.id)
    context = get_shared_context()
    context['form'] = ask_form
    return render(request, "ask.html", context=context)

def login(request):
    if request.method == 'GET':
        login_form = forms.LoginForm()
    elif request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse("index"))
            else:
                login_form.add_error(None, "Username or password is incorrect")
    context = get_shared_context()
    context['form'] = login_form
    return render(request, "login.html", context=context)

def register(request):
    if request.method == 'GET':
        reg_form = forms.RegistrationForm()
    elif request.method == 'POST':
        reg_form = forms.RegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse("index"))
            else:
                reg_form.add_error(None, "User saving error")
    context = get_shared_context()
    context['form'] = reg_form
    return render(request, "register.html", context=context)

@login_required
def settings(request):
    if request.method == 'GET':
        dict_model_fields = model_to_dict(request.user)
        # инициализация формы существующими значениями
        user_form = forms.SettingsForm(initial=dict_model_fields)
    elif request.method == 'POST':
        print("request.POST = ", request.POST)
        print("request.POST = ", request)
        user_form = forms.SettingsForm(data=request.POST, instance = request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse("settings"))
    context = get_shared_context()
    context['form'] = user_form
    return render(request, "settings.html", context=context)

def logout(request):
    auth.logout(request)
    return login(request)

def tag(request, tag_id : int):
    if not models.Tag.objects.filter(pk=tag_id).exists():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    questions = models.Question.objects.get_questions_by_tag(tag_id)
    page = paginate(questions, request)
    context = get_shared_context()
    context['question'] = questions
    context['tag'] = context['tag'] = models.Tag.objects.get(id=tag_id).title
    context['page'] = page
    return render(request, "tag.html", context=context)

