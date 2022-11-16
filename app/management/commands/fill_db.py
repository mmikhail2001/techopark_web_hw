import datetime
import random

from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from app import models


class Command(BaseCommand):
    help = 'Command to do........'
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('-r', '--ratio', type=int, help='ratio of filling db')

    def handle(self, *args, **kwargs):
        try:
            ratio = kwargs["ratio"]
            print("filling...")
            # self.fill_tags(ratio * 1)
            # self.fill_users(ratio * 1)
            # self.fill_answers(ratio * 100)
            # self.fill_likes(ratio * 200)
            self.fill_tags(ratio * 3)
            self.fill_users(ratio * 3)
            self.fill_questions(ratio * 10)
            self.fill_answers(ratio * 30)
            self.fill_likes(ratio * 100)
            print("finish of filling!")

        except Exception as e:
            print("e")
            CommandError(repr(e))
            
    # 1
    def fill_tags(self, n):
        tags = []
        for i in range(n):
            tags.append(models.Tag(title=f'tag{i + 20}'))
        models.Tag.objects.bulk_create(tags)
    
    # 1 
    def fill_users(self, n):
        profiles = []
        users = []
        start_pk_new_users =  max([u.pk for u in models.User.objects.all()]) + 1
        user_first = models.User(username=f'username{0}', password='1Q2w3e4r5t_')
        user_first.save()
        pk_user_first = user_first.pk
        for i in range(n)[1:]:
            users.append(models.User(username=f'username{i}', password='1Q2w3e4r5t_'))
        models.User.objects.bulk_create(users)
        for id in range(n):
            user_id = id + pk_user_first
            profiles.append(models.Profile(user_id=user_id))
        models.Profile.objects.bulk_create(profiles)
            
    
    # почему теги можно добавлять только к сохраненным вопросам?
    # 10
    def fill_questions(self, n):
        questions = []
        count_questions_before =  models.Question.objects.all().count()
        for i in range(n):
            author = random.choice(models.Profile.objects.all())
            questions.append(models.Question(
                title = f'Question tittle {i}', 
                text = f'How can I drink {i} liters of milk?', 
                author = author, 
                date = self.fake.date_time_between(start_date='-5y', end_date='now')
                ))
        models.Question.objects.bulk_create(questions)
        
        for q in models.Question.objects.all()[count_questions_before : ]:
            list_random_tags = random.sample(list(models.Tag.objects.all()), random.randint(1, 10))
            q.tags.set(list_random_tags)

    # 100
    def fill_answers(self, n):
        answers = []
        for i in range(n):
            answers.append(models.Answer(
                text = f'Answer text number {i}',
                date = self.fake.date_time_between(start_date='-5y', end_date='now'),
                is_correct = False,
                author = random.choice(models.Profile.objects.all()),
                question = random.choice(models.Question.objects.all()),
                ))
        models.Answer.objects.bulk_create(answers)
    # 200
    def fill_likes(self, n):
        for i in range(n):
            q = random.choice(models.Question.objects.all())
            p = random.choice(models.Profile.objects.all())
            q.likes.add(p)