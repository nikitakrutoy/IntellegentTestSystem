from django.db import models


class QuestionManager(models.Manager):
    def new():
        pass
    def popular():
        pass

class Tags(models.Model):
    name = models.CharField(max_length = 80, null=True)


class Question(models.Model):
    text = models.TextField()
    complexity = models.IntegerField(default = 0)
    answers = models.TextField(null=True)
    tags = models.ManyToManyField(Tags)
    class Meta:
        db_table = 'question'

class Session(models.Model):
    name = models.CharField(max_length = 80)
    questions = models.ManyToManyField(Question)
    top_border = models.IntegerField(default=0)
    bottom_border = models.IntegerField(default=0)
    limit_sum = models.IntegerField(default=0)
    class Meta:
        db_table = "session"


class OnlineSession(models.Model):
    session = models.ForeignKey(Session)
    mask = models.TextField(default = "")
    question_list = models.TextField(default = "")
    answers_list = models.TextField(default = "")
    right_list = models.TextField(default = "")
    current_questions=models.ManyToManyField(Question, null=True)
    current_question_num=models.IntegerField(default=1)
    user_result = models.IntegerField(default = 0)
    msg_id = models.IntegerField(null=True)
    class Meta:
        db_table = "onlinesession"


class User(models.Model):
    telegram_name = models.TextField(null = True);
    online_session = models.OneToOneField(OnlineSession, null=True)
    status = models.IntegerField(default = 0)
    created_sessions = models.ManyToManyField(Session)
    menu_msg_id = models.IntegerField(null = True)
    class Meta:
        db_table = "user"



class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    class Meta:
        db_table = 'answer'
