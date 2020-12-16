from django.db import models
from django.utils import timezone
# Create your models here.


class User(models.Model):

    FName = models.CharField(max_length=30)
    LName = models.CharField(max_length=30)
    Email = models.EmailField(max_length=30, primary_key=True)
    Mobile = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)
    Image = models.ImageField(upload_to='author_image/', default="")

    def __str__(self):
        return self.Email

class Subject(models.Model):
    Subject_id = models.CharField(max_length=20)
    Subject_name = models.CharField(max_length=150)

    def __str__(self):
        return self.Subject_name


class Topictag(models.Model):
    Topic_id = models.CharField(max_length=25)
    Topic_name = models.CharField(max_length=30)

    def __str__(self):
        return self.Topic_name


class Question(models.Model):
    Question_id = models.CharField( max_length=20, primary_key=True)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Question_approval = models.BooleanField(default=False)
    Question_number = models.CharField(max_length=10)
    Question_title = models.CharField(max_length=150)
    Question_discription = models.CharField(max_length=10000)

    def __str__(self):
        return self.Question_number


class Question_topic(models.Model):
    Question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    Topic_id = models.ForeignKey(Topictag, on_delete=models.CASCADE)

    def __str__(self):
        return self.Question_id.Question_number + " | " + self.Topic_id.Topic_name


class comment(models.Model):
    Question_id = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)
    comment_id = models.CharField( max_length=20, default=None)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank='True')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.Author) + ', ' + self.Question_id.Question_title[:8]

