from django.db import models

class QuestionManager(models.Manager):
    def new():
        pass
    def popular():
        pass

class Tags(models.Model):
    pass

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    telegram_id = models.TextField();
    class Meta:
        db_table = "user"


class Session(models.Model):
    session_id = models.IntegerField(primary_key=True)
    questions = models.ManyToManyField(Question)
    class Meta:
        db_table = "session"

class Question(models.Model):
    objects= QuestionManager();
    question_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    complexity = models.IntegerField(default = 0)
    author = models.ForeignKey(User)
    class Meta:
        db_table = 'question'
        ordering = ['-added_at']

class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    class Meta:
        db_table = 'answer'
