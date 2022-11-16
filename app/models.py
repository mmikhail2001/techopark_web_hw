from django.db import models
from django.contrib.auth.models import User
import random
from django.db.models import Count

class QuestionManager(models.Manager):
    def get_new_questions(self):
        return self.order_by('-date')
    def get_hot_questions(self):
        # добавляем "служебное поле"
        q = self.annotate(Count('likes'))
        q_sort_by_likes = q.order_by('-likes__count')
        return q_sort_by_likes
    def get_single_question(self, idx):
        return self.get(id=idx)
    def get_questions_by_tag(self, idx):
        return self.filter(tags__id=idx)
    
    
class TagManager(models.Manager):
    def get_popular_tags(self):
        t = self.annotate(Count('question'))
        t_sort_by_usage = t.order_by('-question__count')
        return t_sort_by_usage
    def get_single_tag(self, idx):
        return self.get(id=idx)
    
class ProfileManager(models.Manager):
    def get_best_profiles(self):
        p = self.annotate(Count('question'))
        p_sort_by_questions = p.order_by('-question__count')
        return p_sort_by_questions
    def get_single_profile(self, idx):
        return self.get(id=idx)
    

# user's pass: 1Q2w3e4r5t_
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatars/")

    objects = ProfileManager()
    
    def __str__(self):
        return f'Profile #{self.pk}. {self.user.username}'



class Tag(models.Model):
    title       = models.CharField(max_length=30, unique=True)
    objects = TagManager()
    
    def __str__(self):
        return f'Tag #{self.pk}. {self.title}'


class Question(models.Model):
    title       = models.CharField(max_length=200)
    text        = models.TextField(blank=True, null=True)
    # default=timezone.now
    date        = models.DateTimeField() #auto_now_add=True
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags        = models.ManyToManyField(Tag)
    likes       = models.ManyToManyField(Profile, related_name='related_likes')
    
    objects = QuestionManager()
    
    def __str__(self):
        return f'Question #{self.pk}. {self.title}'
    

class Answer(models.Model):
    text        = models.TextField()
    date        = models.DateTimeField() # auto_now_add=True
    is_correct  = models.BooleanField(default=False)
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Answer #{self.pk}. {self.text[:10]}'
                                                                 
# Create your models here.
