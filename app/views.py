from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from . import models

COUNT_BEST_ITEMS = 10

def paginate(objects_list, request, per_page = 5):
    contact_list = objects_list
    paginator = Paginator(contact_list, per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page

def get_question_by_id(id):
    q = models.Question.objects.get_single_question(id)
    q_dict = {
        'id' : q.id,
        'title' : q.title,
        'text' : q.text,
        'author' : q.author.user.username,
        'date' : q.date.strftime("%Y.%m.%d %H:%M"),
        'count_likes' : q.likes.all().count(),
        'tags' : [
            {
                'tag_id' : t.id,  
                'text' : t.title
            } for t in q.tags.all()
        ],
        'answers' : [
            {
                'id' : a.id,
                'text' : a.text,
                'author' : a.author.user.username, 
                'is_correct' : a.is_correct
            } for a in q.answer_set.all()
        ], 
    }
    return q_dict
    
    
def get_list_new_questions_from_db():
    questions = [
        get_question_by_id(q.id)
        for q in models.Question.objects.get_new_questions()
    ]
    return questions


def get_list_hot_questions_from_db():
    questions = [
        get_question_by_id(q.id)
        for q in models.Question.objects.get_hot_questions()
    ]
    return questions

def get_list_questions_by_tag(id):
    questions = [
        get_question_by_id(q.id)
        for q in models.Question.objects.get_questions_by_tag(id)
    ]
    return questions

def get_title_tag_by_id(id):
    return models.Tag.objects.get(id=id).title

def get_list_popular_tags_from_db(id):
    tags = models.Tag.objects.get_popular_tags

def get_tag_by_id(id):
    t = models.Tag.objects.get_single_tag(id)
    t_dict = {
        'id' : t.id,
        'title' : t.title,
    }
    return t_dict

def get_list_popular_tags_from_db():
    tags = [
        get_tag_by_id(t.id)
        for t in models.Tag.objects.get_popular_tags()[:COUNT_BEST_ITEMS]
    ]
    # tags = tags[:COUNT_BEST_ITEMS]
    return tags

def get_profile_by_id(id):
    p = models.Profile.objects.get_single_profile(id)
    p_dict = {
        'id' : p.user.id,
        'username' : p.user.username,
    }
    return p_dict

def get_list_best_profiles_from_db():
    profiles = [
        get_profile_by_id(p.id)
        for p in models.Profile.objects.get_best_profiles()[:COUNT_BEST_ITEMS]
    ]
    # profiles = profiles[:COUNT_BEST_ITEMS]
    return profiles

def get_best_items():
    best_items = {
        'tags' : get_list_popular_tags_from_db(),
        'profiles' : get_list_best_profiles_from_db()
    }
    return best_items


# headers = request.headers
# return HttpResponse(str(headers))
@require_GET
def index(request):
    questions = get_list_new_questions_from_db()
    page = paginate(questions, request)
    context = { 'questions' : questions, 'best_items' : get_best_items(), 'page' : page, 'is_auth' : True, 'is_hot' : False }
    return render(request, "index.html", context=context)

def hot(request):
    hot_questions = get_list_hot_questions_from_db()
    page = paginate(hot_questions, request)
    context = { 'questions' : hot_questions, 'best_items' : get_best_items(), 'page' : page, 'is_auth' : True, 'is_hot' : True }
    return render(request, "hot.html", context=context)

def question(request, question_id : int):
    if not models.Question.objects.filter(pk=question_id).exists():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    questions = get_list_new_questions_from_db()
    needed_question = next(filter(lambda q : q['id'] == question_id, questions))
    answers = needed_question.get('answers')
    page = paginate(answers, request)
    context = { 'question' : needed_question, 'best_items' : get_best_items(), 'page' : page }
    return render(request, "question.html", context=context)

def ask(request):
    context = { 'best_items' : get_best_items(), 'is_auth' : False }
    return render(request, "ask.html", context=context)

def login(request):
    context = { 'best_items' : get_best_items(), 'is_auth' : False }
    return render(request, "login.html", context=context)

def register(request):
    context = { 'best_items' : get_best_items(), 'is_auth' : False }
    return render(request, "register.html", context=context)

def settings(request):
    context = { 'best_items' : get_best_items(), 'is_auth' : False }
    return render(request, "settings.html", context=context)

def tag(request, tag_id : int):
    if not models.Tag.objects.filter(pk=tag_id).exists():
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    questions = get_list_questions_by_tag(tag_id)
    page = paginate(questions, request)
    context = { 'question' : questions, 'best_items' : get_best_items(), 'tag' : get_title_tag_by_id(tag_id), 'page' : page }            
    return render(request, "tag.html", context=context)

# Create your views here.
