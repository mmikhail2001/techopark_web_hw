from django.db import models
from django.contrib.auth.models import User
import random

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    # avatar = models.ImageField(blank=True, null=True, upload_to="", default="")

class Tag(models.Model):
    title       = models.CharField(max_length=30, unique=True)

class Question(models.Model):
    title       = models.CharField(max_length=200)
    text        = models.TextField()
    date        = models.DateTimeField()
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags        = models.ManyToManyField(Tag)
    
class Like(models.Model):
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
class Answer(models.Model):
    text        = models.TextField()
    date        = models.DateTimeField(auto_now_add=True)
    is_correct  = models.BooleanField(default=False)
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)

# QUESTIONS = [
#     { 
#      "id"       : question_id,
#      'title'    : f'Question #{question_id}',
#      'text'     : f'Text of Question #{question_id}',
#      'tags' : [
#         {
#             'tag_id' : id,
#             'text' : f'tag{id}'
#         } for id in list(set([random.randint(0, 10) for _ in range(random.randint(1, 10))]))
#         ],
#      'answers' : [
#         {
#             'id'            : answer_id,
#             'text'          : f'Text of Answer #{answer_id}',
#             'is_correct'    : answer_id == 1,
#         } for answer_id in range(random.randint(1, 10))
#      ],
#     } for question_id in range(20)
# ]

# BEST_ITEMS = {
#     'popular_tags' : [
#         {
#             'tag_id' : id,
#             'text' : f'tag{id}'
#         } for id in [random.randint(0, 10) for _ in range(random.randint(1, 10))]
#         ],
#     'best_users' : [
#         f'Name{i} Surname{i * i}' for i in range(5)
#     ]
# }



# Create your models here.
