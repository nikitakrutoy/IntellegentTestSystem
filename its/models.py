from django.db import models

class QuestionManager(models.Manager):
    def new():
        pass
    def popular():
        pass

class Tags(models.Model):
    pass


class Question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    complexity = models.IntegerField(default = 0)
    answers = models.CharField(max_length=255, choices=[], null=True)
    # author = models.ForeignKey(User)
    class Meta:
        db_table = 'question'

class Session(models.Model):
    id = models.IntegerField(primary_key=True)
    questions = models.ManyToManyField(Question)
    top_border = models.IntegerField(default=0)
    bottom_border = models.IntegerField(default=0)
    class Meta:
        db_table = "session"


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    telegram_id = models.TextField();
    current_session = models.ForeignKey(Session, null=True)
    current_session_questions = models.TextField(null=True)
    class Meta:
        db_table = "user"


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    class Meta:
        db_table = 'answer'
