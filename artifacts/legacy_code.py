class Like(models.Model):
    question    = models.ForeignKey(Question, on_delete=models.CASCADE)
    author      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return f'Like: {self.author.user.username} -> {self.question.title}'

# сортировка по лайкам на pyhton
def get_list_hot_questions_from_db_test():
    questions_likes = [ 
                    {
                        'question_id' : q.id, 
                        'count_likes' : q.like_set.all().count()
                    } for q in models.Question.objects.all()
            ]
    sorted_by_likes = sorted(questions_likes, reverse=True, key = lambda elem : elem['count_likes'])   

    indices_questions = [elem['question_id'] for elem in sorted_by_likes]
    
    hot_questions = [
        get_question_by_id(i)
        for i in indices_questions
    ]

    return hot_questions