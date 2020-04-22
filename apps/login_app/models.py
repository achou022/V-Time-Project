from django.db import models
from django.views.generic.base import TemplateView
import re
from datetime import date, datetime
from django.contrib import messages
import bcrypt
import plotly.offline as opy
import plotly.graph_objs as go

#-----------------------Managers-------------------------#
class UserManager(models.Manager):
    errors={}
    def email_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            return True
        return False 
    def register_validator(self, postData):
        self.errors = {}
        if len(postData['first_name'])<2:
            print('firstName: '+postData['first_name'])
            self.errors['first_name']="must have more than 2 characters in first name"
        if len(postData['last_name'])<2:
            self.errors['last_name']="must have more than 2 characters in last name"
        if self.email_validator(postData):
            self.errors['email']= "Invalid email address!"
        allUsers=User.objects.all()
        for user in allUsers:
            if postData['email']==user.email:
                self.errors['emailUnique']="Email is already in use"
        if len(postData['password_initial'])<2:
            self.errors['passwordlen']="password must be >2 char"
        if postData['password_initial']!=postData['password_verify']:
            self.errors['password']="passwords must match"
        allUsers=User.objects.all()
        for user in allUsers:
            if postData['email']==user.email:
                self.errors['emailUnique']="Email is already in use"
        today=datetime.now()
        birthday=datetime.strptime(postData['birthday'],'%Y-%m-%d')
        if (today-birthday).days<4745: #this many days in 13 years
            self.errors['birthdayValid']="Must be >13"
        return self.errors
    def login_validator(self, postData):
        self.errors = {}
        if self.email_validator(postData):
            self.errors['email']= "Invalid email address!"
        user = User.objects.filter(email=postData['email'])
        if user:
            if 'userlogged' in self.errors:
                del self.errors['userlogged'] #clear error dictionary after page refresh
            logged_user = user[0] 
            if bcrypt.checkpw(postData['password'].encode(), logged_user.pw.encode()):
                if 'userpass' in self.errors:
                    del self.errors['userpass'] #clear error dictionary after page refresh
            else:
                self.errors['userpass']= "Invalid username or password" 
        else: self.errors['userlogged']= "Invalid username or password"    
        return self.errors
    def edit_validator(self, postData, my_id):
        self.errors  = {}
        if len(postData['first_name'])<2:
            self.errors['first_name']="edit: must have more than 2 characters in first name"
        if len(postData['last_name'])<2:
            self.errors['last_name']="edit: must have more than 2 characters in last name"
        if self.email_validator(postData):
            self.errors['email']= "edit: Invalid email address!"
        # allUsers = User.objects.all()
        # for user in allUsers:
        #     if user.id != my_id:
        #         if postData['email']==user.email:
        #             self.errors['emailUnique']="Email is already in use"
        return self.errors
#-----------------------Models-------------------------#
class User(models.Model):
    # user methods===============================================================
    def __repr__(self):
        return f"< Item from User table: {self.first_name}>"

    # returns all upcoming events, filter with datetime.now
    def upcomingEvents(self, n=5):
        return self.jobs.all().filter(event__time__gt=datetime.now())[:n]

    def allFutureEvents(self):
        return self.jobs.all().filter(event__time__gt=datetime.now())

    # returns past 5 events that has expired/participated
    def pastEvents(self, n=5):
        return self.jobs.all().filter(event__time__lt=datetime.now())[:n]

    def allPastEvents(self):
        return self.jobs.all().filter(event__time__lt=datetime.now())

    def powerUser(self):
        pu=User.objects.first()
        for user in User.objects.all():
            max=pu.vTime()
            if user.vTime() > max:
                pu=user
        return pu

    # returns the total amount of volunteer time
    def vTime(self):
        return sum(job.hours for job in self.jobs.all().filter(event__time__lt=datetime.now()))

    def avgVTime(self):
        return round(self.vTime()/len(self.jobs.all()), 1)

    # returns the 3 most recent post created by the user
    def recentPosts(self, n=3):
        return self.user_post.all().order_by('created_at').reverse()[:n]

    # returns the 3 most recent comment created by the user
    def recentComments(self, n=3):
        return self.user_comment.all().order_by('created_at').reverse()[:n]

    # returns a basic acitivity level line graph (output:div)
    def visualStat(self):
        x=[]
        y=[]
        for job in self.jobs.all().filter(event__time__lt=datetime.now()):
            print(job)
            x.append(job.event.name)
            y.append(job.hours)
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'blue', 'symbol': 105, 'size': 14},
                            mode="lines",  name='1st Trace')
        data=go.Data([trace1])
        layout=go.Layout(title=f"{self.first_name} {self.last_name}'s Volunteer Activity", xaxis={'title':''}, yaxis={'title':'Volunteer Hours'})
        figure=go.Figure(data=data,layout=layout)
        # resizes the chart for modal
        figure.update_layout(
            autosize=False,
            width=450,
            height=300,
            margin=dict(
                l=50,
                r=50,
                b=60,
                t=60,
                pad=2
            )
        )
        div = opy.plot(figure, auto_open=False, output_type='div')
        return div
    # user fields=============================================================
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=90)
    alias = models.CharField(max_length=45)
    pw = models.CharField(max_length=90)
    birthday = models.DateTimeField()
    level = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=15) #check out Twilio
    description = models.CharField(max_length=150, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #foreign key 'company_admin'
    #foreign key 'jobs'
    #foreign key 'user_post'
    #foreign key 'user_comment'