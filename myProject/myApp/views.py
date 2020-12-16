import secrets
import string
from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages


# ************************** Import for Extractor ********************************************

import time, re, json, numpy as np, sys, csv
from sklearn.svm import LinearSVC
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
import joblib
from nltk.stem.snowball import SnowballStemmer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
from django.contrib.staticfiles.storage import staticfiles_storage
import os

# ********************************************************************************************

# Create your views here.
from django.contrib.auth.models import User, auth
from .models import Question, User, Question_topic, Subject, Topictag


s = set(stopwords.words('english'))
stemmer = SnowballStemmer('english', ignore_stopwords=True)
count = 0
#tagrows=fh.read().split('\n')[:248000]
#checktags=[]
#X=fh2.read().split('\n')[:248000]
p = os.path.abspath('myApp/static/myApp/tag_extract/clf.txt')
q = os.path.abspath('myApp/static/myApp/tag_extract/multibin.txt')
classifier = joblib.load(p)
multibin = joblib.load(q)
vectorizer_2 = CountVectorizer()


def predictTags(question):
    T = []
    #words = str(self.lineEdit.text())+' '+str(self.plainTextEdit.toPlainText())
    # words=input("Enter question:")
    words = question
    words = re.sub('\n', ' ', words)
    words = re.sub('[!@%^&*()$:"?<>=~,;`{}|]', ' ', words)
    words = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?]))''',' ',words)
    words = re.sub('_', '-', words)
    words = words.replace('[', ' ')
    words = words.replace(']', ' ')
    words = words.replace('/', ' ')
    words = words.replace('\\', ' ')
    words = re.sub(r'(\s)\-+(\s)', r'\1', words)
    words = re.sub(r'\.+(\s)', r'\1', words)
    words = re.sub(r'\.+\.(\w)', r'\1', words)
    words = re.sub(r'(\s)\.+(\s)', r'\1', words)
    words = re.sub("'", '', words)
    words = re.sub(r'\s\d+[\.\-\+]+\d+|\s[\.\-\+]+\d+|\s+\d+\s+|\s\d+[\+\-]+',' ',words)
    words = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", words)
    words = re.sub(r'\s\#+\s|\s\++\s',' ',words)
    stemmed_words = [stemmer.stem(word) for word in words.split()]
    clean_text = filter(lambda w: not w in s, stemmed_words)
    words = ''
    for word in clean_text:
            words += word+' '
    T.append(words)
    print("T", T)
    results = classifier.predict(T)
    results=multibin.inverse_transform(results)
    #print '\n',results,'\n'
    buff = ''
    tagarr=[]
    for result in results[0]:
            #buff=buff+QString(result)+' ; '
            tagarr.append(result)
    #self.lineEdit_2.setText(buff[:len(buff)-3])
    #recommend()
    print(tagarr)
    return tagarr


def index(request):
    ques = Question_topic.objects.all()
    if request.session.get('session_name'):
        user = User.objects.get(Q(Email=request.session.get('session_name')))
        return render(request, 'myApp/home.html', {'user': user, 'ques': ques} )
    return render(request, 'myApp/home.html', {'user': request.session.get('session_name'), 'ques': ques})


def temp(request):
    auth.logout(request)
    return redirect('index')


def signin_page(request):
    if request.session.get('session_name'):
        user = User.objects.get(Q(Email=request.session.get('session_name')))
        print(user.Email)
        return render(request, 'myApp/add_question.html',  {'user': user})

    return render(request, 'myApp/signin.html', {'user': request.session.get('session_name')})


def signup_page(request):
    if request.session.get('session_name'):
        user = User.objects.get(Q(Email=request.session.get('session_name')))
        print(user.Email)
        return render(request, 'myApp/add_question.html',  {'user': user})

    return render(request, 'myApp/signup.html', {'user': request.session.get('session_name')})


# def login(request):
#     return render(request, 'myApp/add_question.html')

def login(request):
    try:
        if request.method == 'POST':
            uname = request.POST['username']
            lpass = request.POST['password']
            ob = User.objects.get(Q(Email=uname))
            if ob.Password == lpass:
                request.session['session_name'] = uname
                return redirect('home')
            else:
                return redirect('signin_page')
        else:
            return redirect('signin_page')
    except:
        return redirect('signin_page')


def logout(request):
    auth.logout(request)
    return redirect('index')


def signup(request):
    try:
        print("rrrrrrrrrrrrrrrrrrrrrr")
        if request.method == 'POST':

            first_Name = request.POST['fname']
            last_Name = request.POST['lname']
            email = request.POST['email']
            mobile = request.POST['mobile']
            password = request.POST['password']
            confirm_password = request.POST['confpassword']
            pro_pic = request.FILES['profile_pic']
            print("0")

        else:
            return render(request, 'myApp/signin.html')
        print("1")
        if password != confirm_password:
            notification = {
                'note': "Password didn't match !!",
                'f_n': first_Name,
                'l_n': last_Name,
                'm_no': mobile,
                'mail': email,
                'img': pro_pic
            }
            print("Password didn't match !!")
            messages.error(request, 'Password didnt match !')
            return render(request, 'myApp/signup.html', notification)

        obj = User.objects.filter(Q(Email=email)).first()
        if obj is not None:
            notification = {
                'note': "Email already exists.. !!",
                'f_n': first_Name,
                'l_n': last_Name,
                'm_no': mobile,
                'img': pro_pic
            }
            print("Email already exists.. !!")
            messages.error(request, 'Email already exists.. !!')
            return render(request, 'myApp/signup.html', notification)
        user = User(
            FName=first_Name,
            LName=last_Name,
            Email=email,
            Mobile=mobile,
            Password=password,
            Image=pro_pic,
        )
        user.save()
        print("2")
        messages.success(request, 'Registered Successfully')
        return redirect('login')

    except:
        print("eeeeeeeeeeeeeeeeee")
        return redirect('signup_page')


def dpupdate(request):
    if request.method == 'POST':
        pro_pic = request.FILES['dp']
        user = User.objects.get(Q(Email=request.session.get('session_name')))
        user.Image = pro_pic
        user.save()
        print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
        return redirect('profile')
    return redirect('profile')



def add_question(request):
    if request.method != 'POST':
        if request.session.get('session_name'):
            user = User.objects.get(Q(Email=request.session.get('session_name')))
            subject = Subject.objects.all()
            return render(request, 'myApp/add_question.html', {'user': user, 'subject': subject})
        return redirect(index)
    quesdata = Question.objects.all()
    q_title = request.POST['title']
    q_sub = request.POST['subj']
    q_decr = request.POST['description']
    sub_obj = Subject.objects.get(Q(Subject_name=q_sub))
    user_obj = User.objects.get(Q(Email=request.session.get('session_name')))
    q_no = quesdata.count()+101
    question = Question(
        Question_title=q_title,
        Question_discription=q_decr,
        Subject=sub_obj,
        Author=user_obj,
        Question_number=q_no,
        Question_id=''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(15))
    )
    question.save()

    tagarr = predictTags((q_title+" ")*5 + (q_decr+" ")*3)
    print(len(tagarr))
    if( len(tagarr) == 0):
        fsttag = Topictag.objects.get(Topic_id="N/A")
        fstobj = Question_topic(
            Question_id=question,
            Topic_id=fsttag
        )
        fstobj.save()
        return HttpResponse( "added sucessfully............[N/A]" )
    tagdata = Topictag.objects.all()
    for tag in tagarr:
        for t in tagdata:
            flag = 0
            if t.Topic_name == tag:
                flag = 1
                break
        if flag == 0:
            tagobj = Topictag(
                Topic_id=''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(15)),
                Topic_name=tag
            )
            tagobj.save()
            tagquesobj = Question_topic(
                Question_id=question,
                Topic_id=tagobj
            )
            tagquesobj.save()
        else:
            tagquesobj = Question_topic(
                Question_id=question,
                Topic_id=t
            )
            tagquesobj.save()





    # print(predictTags(q_title*5 + q_decr*3))
    # question.save()
    return HttpResponse( "added sucessfully............" )
    # return HttpResponse()


def home(request):
    # for v in Question_topic.objects.annotate(value=F('vote__value'), year=F('vote__year')).values('name', 'value', 'year'):
    #     print(v)
    # ques = Question.objects.filter(Q(Question_approval=True))
    ques = Question_topic.objects.all()
    if request.session.get('session_name'):
        user = User.objects.get(Q(Email=request.session.get('session_name')))
        return render(request, 'myApp/home.html', {'user': user, 'ques': ques})
    return render(request, 'myApp/home.html', {'user': request.session.get('session_name'), 'ques': ques})


def search(request):
    inputtext = request.POST['text_input']
    searchby = request.POST['searchby']
    if request.session.get('session_name'):
        user = User.objects.get(Q(Email=request.session.get('session_name')))
    else:
        user = request.session.get('session_name')
    if searchby == '--select--':
        print(4)
        return redirect(home)

    if searchby == 'q_no':
        question = Question.objects.filter(Question_number=inputtext, Question_approval=True)
        print(1)
        ques = None
        if question.count() > 0:
            ques = Question_topic.objects.filter(Question_id=question[0])
        print(ques)
        return render(request, 'myApp/home.html', {'user': user, 'ques': ques})

    elif searchby == "tag":
        tag = Topictag.objects.filter(Topic_name=inputtext)
        ques = None
        if tag.count() > 0:
            ques = Question_topic.objects.filter(Q(Topic_id=tag[0]))
        return render(request, 'myApp/home.html', {'user': user, 'ques': ques})

    elif searchby == "subject":
        sub = Subject.objects.get(Subject_name=inputtext)
        ques = Question.objects.filter(Subject=sub, Question_approval=True)
        print(3)
        return render(request, 'myApp/home.html', {'user': user, 'ques': ques})
    else:
        print(5)
        return redirect(home)


def profile(request):
    if request.session.get('session_name'):
        user = User.objects.get(Q(Email=request.session.get('session_name')))
        ques = Question.objects.filter(Q(Author=user))
        # q2 = Question_topic.objects.all()
        # ques = q2.intersection(q1)

        return render(request, 'myApp/profile.html', {'user': user, 'ques': ques})
    return redirect(index)


def question_view(request, id=None):
    user = request.session.get('session_name')
    if(request.session.get('session_name')):
        user = User.objects.get(Q(Email=request.session.get('session_name')))
    ques = Question.objects.get(Q(Question_id=id))
    tags = Question_topic.objects.filter(Q(Question_id=ques))
    return render(request, 'myApp/questionview.html', {'user': user, 'ques': ques, 'tags': tags})


def tagsearch(request, tag_id=None):
    if request.session.get('session_name'):
        user = User.objects.get(Q(Email=request.session.get('session_name')))
    else:
        user = request.session.get('session_name')
    tag = Topictag.objects.filter(Topic_id=tag_id)
    ques = None
    if tag.count() > 0:
        ques = Question_topic.objects.filter(Q(Topic_id=tag[0]))
    ''' 
       ques = []
        for q in quesid:
            if(Question.objects.get(Q(Question_id=q.Question_id)).Question_approval==True):
                ques.append(q.Question_id)
    '''
    return render(request, 'myApp/home.html', {'user': user, 'ques': ques})


